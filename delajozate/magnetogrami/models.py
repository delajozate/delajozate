# coding: utf-8
import datetime
import dateutil.parser
import json
import logging
import os
import pytz
import re
import requests
import time
import urllib

try:
    from collections import OrderedDict
except ImportError:
    from django.utils.datastructures import SortedDict as OrderedDict

from django.db import models, transaction, connection
from django.core.urlresolvers import reverse

from delajozate.dz.models import Oseba, Mandat, DelovnoTelo, Stranka, Pozicija
from delajozate.search.simple import SearchModel

datalogger = logging.getLogger('data')

GLASOVI = (
    ('0', 'Proti'),
    ('1', 'Za'),
    ('2', 'Ni glasoval'),
)

class Seja(models.Model):
    naslov = models.CharField(max_length=2000)
    seja = models.CharField(max_length=255) # TODO: check validity
    slug = models.CharField(max_length=100, db_index=True)
    datum_zacetka = models.DateField(null=True, db_index=True)
    status = models.CharField(max_length=128)
    mandat = models.IntegerField()
    delovno_telo = models.CharField(max_length=20)
    url = models.URLField()

    class Meta:
        ordering = ('-mandat', '-datum_zacetka',)

    def __unicode__(self):
        return self.naslov

    def magnetogrami(self):
        return Zasedanje.objects.filter(seja=self).filter(models.Q(tip='magnetogram') | models.Q(tip='dobesednizapis')).select_related('seja')

class Zasedanje(models.Model):
    seja = models.ForeignKey(Seja)
    naslov = models.CharField(max_length=255, null=True)
    datum = models.DateField(null=True, db_index=True)
    zacetek = models.TimeField(null=True)
    konec = models.TimeField(null=True)
    url = models.URLField(null=True)
    tip = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('-datum',)

    def __unicode__(self):
        return self.seja.naslov + " (" + str(self.datum) + ")"

    @models.permalink
    def get_absolute_url(self):
        return ('delajozate.magnetogrami.views.seja', None, {'mdt': self.seja.delovno_telo, 'mandat': self.seja.mandat, 'slug': self.seja.slug, 'datum_zasedanja': self.datum} )

    def stranke():
        def fget(self):
            try:
                return self.__stranke
            except AttributeError:
                clanstvo = Pozicija.objects.filter(
                    organizacija__stranka__isnull=False,
                    oseba__id__in=[i.govorec_oseba.pk for i in self.zapis_set.all().select_related('govorec_oseba', 'zasedanje') if i.govorec_oseba is not None],
                    od__lte=self.datum,
                    do__gt=self.datum
                    ).select_related("oseba", "stranka")
                self.__stranke = dict([(i.oseba.pk, i.organizacija.value()) for i in clanstvo])
                return self.__stranke
        return (fget,)
    stranke = property(*stranke())

class Video(models.Model):
    title = models.CharField(max_length=512)
    datum = models.DateField()
    url = models.CharField(max_length=512)
    ava_id = models.CharField(max_length=512, unique=True)
    zasedanje = models.ForeignKey(Zasedanje, null=True)

    class Meta:
        ordering = ('-datum',)

    def __unicode__(self):
        return self.title

    def upari(self):
        "FIXME: improvements, maybe?"
        qs = Zasedanje.objects.filter(datum=self.datum)

        m = re.match('^\s*(\d+\.)', self.title)
        if m:
            stevilka = m.group(1)
            qs = qs.filter(seja__naslov__contains=stevilka)

        zasedanja = list(qs)
        if len(zasedanja) == 1:
            self.zasedanje = zasedanja[0]
            return True
        return False

class Zapis(models.Model):
    zasedanje = models.ForeignKey(Zasedanje)
    seq = models.IntegerField()
    odstavki = models.TextField(null=True)
    govorec = models.CharField(max_length=255, null=True)
    govorec_oseba = models.ForeignKey(Oseba, null=True)

    class Meta:
        ordering = ('seq',)
        verbose_name = 'Zapis magnetograma'
        verbose_name_plural = 'Zapisi magnetogramov'

    def __unicode__(self):
        if self.govorec:
            return self.govorec + ":" + self.odstavki[0:30]
        else:
            return self.odstavki[0:30]

    @models.permalink
    def get_absolute_url(self):
        return ('delajozate.magnetogrami.views.seja', None, {
            'mdt': self.zasedanje.seja.delovno_telo, 
            'mandat': self.zasedanje.seja.mandat, 
            'slug': self.zasedanje.seja.slug, 
            'datum_zasedanja': self.zasedanje.datum
        })

    def permalink():
        def fget(self):
            return self.get_absolute_url()
        return (fget,)
    permalink = property(*permalink())

    def clan_stranke():
        def fget(self):
            d = self.zasedanje.datum
            return self.govorec_oseba.stranke.filter(od__lte=d, do__gt=d)
        return (fget,)
    clan_stranke = property(*clan_stranke())

    def timestamp():
        def fget(self):
            return self.zasedanje.datum
        return (fget,)
    timestamp = property(*timestamp())

    def govorec_slug():
        def fget(self):
            if self.govorec_oseba:
                slug = self.govorec_oseba.slug
                if slug is None:
                    return u''
                return unicode(slug)
        return (fget,)
    govorec_slug = property(*govorec_slug())

    def govorec_text():
        def fget(self):
            if self.govorec_oseba is not None:
                text = unicode(self.govorec_oseba)
            else:
                text = self.govorec
            return text
        return (fget,)
    govorec_text = property(*govorec_text())

    def ime_seje():
        def fget(self):
            return self.zasedanje.seja.naslov
        return (fget,)
    ime_seje = property(*ime_seje())

class ZapisSearch(SearchModel):
    model = Zapis
    index_fields = ['seq', 'timestamp', 'govorec_text', 'govorec_slug', 'permalink', 'ime_seje']
    hilight = 'odstavki'

    def index_zasedanje(self, zasedanje):
        self.index(items=Zapis.objects.filter(zasedanje__pk=zasedanje.pk).select_related('zasedanje', 'zasedanje__seja', 'govorec_oseba'))

    def get_queryset(self):
        from django.conf import settings

        resp = requests.get(settings.SOLR_URL + 'select?q=*%3A*&sort=datum_timestamp+desc&wt=json')

        dt = datetime.datetime.strptime(resp.json()['response']['docs'][0]['datum_timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        dt = (dt - datetime.timedelta(7))
        return Zapis.objects.filter(zasedanje__datum__gte=dt).order_by('zasedanje__datum')

    def full_index(self):
        from multiprocessing import Process
        for z in Zasedanje.objects.all().order_by('datum'):
            print z.datum
            p = Process(target=self.index_zasedanje, args=(z,))
            p.start()
            p.join()

class Glasovanje(models.Model):
    seja = models.ForeignKey(Seja, null=True)
    ura = models.TimeField(null=True, blank=True)
    url = models.URLField(null=True)
    datum = models.DateField(null=True, blank=True)
    dokument = models.CharField(max_length=2000, null=True)
    naslov = models.CharField(max_length=2000, null=True)
    faza_postopka = models.CharField(max_length=255, null=True)
    zapis = models.ForeignKey(Zapis, null=True, default=None)
    vir_datuma = models.CharField(max_length=20, default='')

    class Meta:
        ordering = ('-seja__mandat', '-datum')
        verbose_name = 'Glasovanje'
        verbose_name_plural = 'Glasovanja'

    def __unicode__(self):
        r = u''
        if self.dokument:
            r = r + self.dokument + ', '
        if self.naslov:
            r += self.naslov
        else:
            r += self.seja.naslov
        return r

    def timestamp(self):
        ts = datetime.datetime(self.datum.year, self.datum.month, self.datum.day, tzinfo=pytz.UTC)
        if self.ura:
            ts = ts.replace(hour=self.ura.hour, minute=self.ura.minute, second=self.ura.second)
        return ts

    @models.permalink
    def absolute_url(self):
        if self.ura:
            return ('glasovanja.views.glasovanje', 
                (self.datum.strftime('%Y-%m-%d'), self.ura.strftime('%H:%M:%S')))
        return ('glasovanja.views.glasovanje', (self.datum, self.id))

    def rezultati():
        def fget(self):
            glasovi = self.glas_set.all()
            k = sum([i.kvorum for i in glasovi])
            z = sum([1 for i in glasovi if i.glasoval == 'Za'])
            p = sum([1 for i in glasovi if i.glasoval == 'Proti'])
            n = sum([1 for i in glasovi if i.glasoval == 'Ni' and i.kvorum])
            od = sum([1 for i in glasovi if i.glasoval == 'Ni' and not i.kvorum])
            return {
                'kvorum': k,
                'za': z,
                'proti': p,
                'ni': n,
                'odsoten': od,
                }
        return (fget,)
    rezultati = property(*rezultati())

    def passed(self):
        self.glas_set.all()
        rez = self.rezultati
        return int(rez['za'] > rez['proti'] + rez['ni'])

    def stranke():
        def fget(self):
            try:
                return self.__stranke
            except AttributeError:
                clanstvo = Pozicija.objects.filter(
                    organizacija__stranka__isnull=False,
                    oseba__id__in=[i.oseba.pk for i in self.glas_set.all().select_related('oseba') if i.oseba],
                    od__lte=self.datum,
                    do__gt=self.datum
                    ).select_related("oseba", "organizacija__stranka")
                self.__stranke = dict([(i.oseba.pk, i.organizacija.value()) for i in clanstvo])
                return self.__stranke
        return (fget,)
    stranke = property(*stranke())

    def summary():
        def fget(self):
            glasovi = list(self.glas_set.all().select_related('oseba', 'glasovanje'))

            rez = self.rezultati


            total_for = total_against = total_absent = total_abstained = 0
            data = {}
            for glas in glasovi:
                try:
                    stranka = self.stranke[glas.oseba.pk]
                    okrajsava = stranka.okrajsava
                except AttributeError:
                    stranka = okrajsava = 'Neznana'
                    datalogger.info('Manjka povezava med poslancem in osebo: "%s". Dodaj preslikavo med govorcem in osebo.' % (glas.poslanec,), exc_info=False)

                except KeyError:
                    stranka = okrajsava = 'Neznana'
                    datalogger.info('Manjka clanstvo stranke za osebo %s (oseba_id=%s)' % (glas.oseba, glas.oseba.id), exc_info=False)

                if not data.get(okrajsava, None):
                    data[okrajsava] = {
                        'stranka': stranka or None,
                        'za': 0,
                        'proti': 0,
                        'abstained': 0,
                        'absent': 0,
                        'count': 0.0,
                        'present': 0.0,
                        'percent': 0
                    }
                if glas.kvorum:
                    if glas.glasoval == 'Za': 
                        data[okrajsava]['za'] += 1
                        total_for += 1
                    elif glas.glasoval == 'Proti': 
                        data[okrajsava]['proti'] += 1
                        total_against += 1
                    if glas.glasoval == 'Ni':
                        data[okrajsava]['abstained'] += 1
                        total_abstained += 1
                    data[okrajsava]['present'] += 1
                else:
                    data[okrajsava]['absent'] += 1
                    total_absent += 1
                data[okrajsava]['count'] += 1

            if total_for >= total_against + total_abstained:
                majority = 'za'
                minority = 'proti'
                majority_voted = total_for
                minority_voted = total_against
            else:
                majority = 'proti'
                minority = 'za'
                majority_voted = total_against
                minority_voted = total_for

            for stranka in data:
                data[stranka]['percent'] =  (data[stranka]['present'] / data[stranka]['count']) * 100

            data_sorted = OrderedDict()
            for key in sorted(data.iterkeys()):
                data_sorted[key] = data[key]
                data_sorted[key]['majority'] = data_sorted[key][majority]
                data_sorted[key]['minority'] = data_sorted[key][minority]

            data_sorted['Skupaj'] = {
                        'stranka': None,
                        'za': total_for,
                        'proti': total_against,
                        'majority': majority_voted,
                        'minority': minority_voted,
                        'abstained': total_abstained,
                        'absent': total_absent,
                        'count': 0.0,
                        'present': (90 - total_absent),
                        'percent': ((90.0 - total_absent) / 90.0 * 100.0),
                    }

            return {
                'majority': majority,
                'minority': minority,
                'votes': data_sorted,
            }
        return (fget,)
    summary = property(*summary())

class GlasovanjeSearch(SearchModel):
    model = Glasovanje
    hilight = 'naslov'
    index_fields = ['dokument', 'naslov', 'faza_postopka', 'timestamp', 'absolute_url', 'passed']

class Glas(models.Model):
    glasovanje = models.ForeignKey(Glasovanje, null=True)
    oseba = models.ForeignKey(Oseba, null=True)
    kvorum = models.BooleanField(default=False)
    glasoval = models.CharField(max_length=255, choices=GLASOVI)
    poslanec = models.CharField(max_length=128)

    def __unicode__(self):
        return u'%s %s %s' % (self.poslanec, self.kvorum, self.glasoval)

    def stranka():
        def fget(self):
            return self.oseba.clanstvo(self.glasovanje.datum)[0].stranka

        return (fget,)
    stranka = property(*stranka())

    class Meta:
        ordering = ('oseba__priimek', 'oseba__ime')


class GovorecMap(models.Model):
    govorec = models.CharField(max_length=200, unique=True, db_index=True)
    oseba = models.ForeignKey(Oseba)

    class Meta:
        verbose_name = u'Preslikava govorec-oseba'
        verbose_name_plural = u'Preslikave govorec-oseba'
    def __unicode__(self):
        return u'"%s" -> %s' % (self.govorec, self.oseba)

    def save(self, *args, **kwargs):
        super(GovorecMap, self).save(*args, **kwargs)

        # posodobi obstojece zapise
        with transaction.commit_on_success():
            transaction.set_dirty()

            cur = connection.cursor()
            # zapisi
            cur.execute('''UPDATE %s SET govorec_oseba_id = %%s WHERE govorec = %%s''' % Zapis._meta.db_table, [self.oseba.id, self.govorec])
            # glasovanja
            cur.execute('''UPDATE %s SET oseba_id = %%s WHERE poslanec = %%s''' % Glas._meta.db_table, [self.oseba.id, self.govorec])

def _parse_time(time_string):
    try:
        parsed_time = time.strptime(time_string, "%H.%S")
    except:
        try:
            parsed_time = time.strptime(time_string, "%H")
        except:
            parsed_time = None

    if parsed_time:
        return time.strftime("%H:%S", parsed_time)
    else:
        return None


def seja_import_one(jsonData):
    govorci_fn = os.path.join(os.path.dirname(__file__), 'govorci.json')

    if jsonData['url'] in (
        'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=IV&seja=24%20025.%20Redna&uid=E55FDF1837852856C1257275002A20A7',
        'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=III&seja=18%20015.%20Redna&uid=BF0C1A3AD3AD5771C1256C7C0035B39E',
        'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=III&seja=20%20013.%20Redna&uid=0485BF77D1915B2AC1256AEA0027F57D',
        'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=III&seja=21%20005.%20Redna&uid=99B38E120CF33D2EC1256A3800491AA2',
        'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=III&seja=18%20002.%20Redna&uid=86E49857111C3DB0C1256A06004F1763',
        'http://www.dz-rs.si/wps/portal/Home/deloDZ/seje/izbranaSejaDt?mandat=II&seja=34%20004.%20Redna&uid=566456472D99E269C125687A002D0AEB',
        ):
        # glupe skupne seje :/
        return
    with transaction.commit_on_success():
        mandat = int(jsonData.get('mandat'))
        naslov_seje = jsonData.get('naslov')
        dt = jsonData.get('delovno_telo')
        try:
            seja = Seja.objects.get(
                mandat=mandat,
                naslov=naslov_seje,
                delovno_telo=dt,
                )
        except Seja.DoesNotExist:
            seja = Seja(mandat=mandat, naslov=naslov_seje, delovno_telo=dt)

        match = re.search(u'((\d+)\s?\.\s*(redna|izredna|nujna|zasedanje|seja izvr.ilnega odbora))', naslov_seje, re.I)
        if not match:
            unquoted_url = urllib.unquote(jsonData.get('url'))
            match = re.search(u'seja=(KPDZ|\d+) 0*(\d+)\.? (redna|izredna|nujna|zasedanje|sre.anje|posvet)', unquoted_url, re.I | re.U)
            if not match:
                print [naslov_seje]
                print jsonData.get('url')
                print naslov_seje

        seja_slug = ('%s-%s' % match.groups()[1:]).lower()
        seja.slug = seja_slug
        try:
            seja.datum_zacetka = dateutil.parser.parse(jsonData.get('datum_zacetka'), dayfirst=True)
        except:
            seja.datum_zacetka = None
        seja.seja = match.group(1)
        seja.url = jsonData.get('url')
        seja.save()

        #Glasovanja
        for jsonGlasovanje in jsonData.get('glasovanja'):

            url = jsonGlasovanje.get("url")
            ura = jsonGlasovanje.get("ura")
            if not ura:
                ura = None
            if jsonGlasovanje.get('datum'):
                datum = dateutil.parser.parse(jsonGlasovanje.get('datum'), dayfirst=True)
            else:
                datum = None
            dokument = jsonGlasovanje.get("dokument")
            naslov = jsonGlasovanje.get("naslov")
            faza_postopka = jsonGlasovanje.get("faza postopka")

            try:
                glasovanje = Glasovanje.objects.get(
                    seja=seja,
                    ura=ura,
                    url=url,
                    datum=datum,
                    dokument=dokument,
                    naslov = naslov,
                    faza_postopka=faza_postopka,
                )
            except Glasovanje.DoesNotExist:
                print datum
                print dokument
                print naslov
                glasovanje = Glasovanje()
                glasovanje.seja = seja
                glasovanje.ura = ura
                glasovanje.url = url
                glasovanje.datum = datum
                glasovanje.dokument = dokument
                glasovanje.naslov = naslov
                glasovanje.faza_postopka = faza_postopka
                glasovanje.save()

            for glas in jsonGlasovanje.get("glasovi"):
                poslanec = glas.get("poslanec")# .encode("utf-8")
                #print [poslanec]
                try:
                    g = GovorecMap.objects.get(govorec=poslanec)
                    oseba = g.oseba
                except GovorecMap.DoesNotExist:
                    sp = poslanec.split()
                    if len(sp) == 2:
                        poslanec_r = u'%s %s' % (sp[1], sp[0])
                        try:
                            g = GovorecMap.objects.get(govorec=poslanec_r)
                            oseba = g.oseba
                        except GovorecMap.DoesNotExist:
                            #print '---- FAIL', [poslanec], poslanec
                            oseba = None
                    else:
                        #print '---- FAIL', [poslanec], poslanec
                        oseba = None

                try:
                    g = Glas.objects.get(
                        glasovanje = glasovanje,
                        poslanec = poslanec
                    )
                    if oseba is not None and g.oseba != oseba:
                        # ob najdeni osebi shrani
                        g.oseba = oseba
                        g.save()
                except Glas.DoesNotExist:
                    g = Glas(
                        glasovanje=glasovanje,
                        kvorum=glas.get('kvorum'),
                        glasoval=glas.get('glasoval'),
                        oseba=oseba,
                        poslanec=poslanec
                        )
                    g.save()

        # Zasedanja
        for jsonZasedanje in jsonData.get('zasedanja'):
            if jsonZasedanje.get('datum') is None:
                continue
            for jsonPovezava in jsonZasedanje.get('povezave'):
                datum = dateutil.parser.parse(jsonZasedanje.get('datum'), dayfirst=True)
                created = False
                try:
                    zasedanje = Zasedanje.objects.get(
                        datum=datum,
                        seja=seja,
                        )
                except Zasedanje.DoesNotExist:
                    zasedanje = Zasedanje(
                        datum=datum,
                        seja=seja,
                        )
                    created = True

                if not created:
                    continue
                if jsonPovezava.get('zacetek'):
                    zasedanje.zacetek = _parse_time(jsonPovezava.get('zacetek'))
                if jsonPovezava.get('konec'):
                    zasedanje.konec = _parse_time(jsonPovezava.get('konec'))

                zasedanje.tip = jsonPovezava.get('tip')
                zasedanje.naslov = jsonPovezava.get('naslov')
                zasedanje.url = jsonPovezava.get('url')
                zasedanje.save()

                cursor = connection.cursor()
                count = 0
                keys = ['seq', 'zasedanje_id', 'govorec', 'govorec_oseba_id', 'odstavki']

                values = []
                for jsonOdsek in jsonPovezava.get('odseki'):
                    for jsonZapis in jsonOdsek.get('zapisi'):
                        govorec = jsonZapis.get('govorec')
                        if govorec is not None:
                            govorec = govorec.strip()
                            m = re.match('^(.*)\s\(PS \w{2,5}\)$', govorec)
                            if m:
                                govorec = m.group(1)
                        try:
                            oseba_id = GovorecMap.objects.get(govorec=govorec).oseba.id
                        except GovorecMap.DoesNotExist:
                            oseba_id = None

                        for ods in jsonZapis.get('odstavki'):
                            values.extend([
                                count,
                                zasedanje.id,
                                govorec,
                                oseba_id,
                                ods,
                                ])
                            count += 1

                params = values
                onerowtempl = '(' + ', '.join(['%s'] * len(keys)) + ')'
                all_rows_template = ', '.join([onerowtempl] * (len(params) / len(keys)))
                sql = '''INSERT INTO %s (%s) VALUES %s''' % (
                    Zapis._meta.db_table,
                    ', '.join(keys),
                    all_rows_template)
                if params:
                    cursor.execute(sql, params)
        if seja.datum_zacetka is None:
            # use as an alternative
            try:
                seja.datum_zacetka = Zasedanje.objects.filter(seja=seja).order_by('-datum')[0].datum
            except:
                pass
        seja.save()
