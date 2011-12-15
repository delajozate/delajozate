import datetime
import dateutil.parser
import json
import os
import re
import sunburnt
import time

from django.db import transaction, connection

import settings
from magnetogrami.models import Seja, SejaInfo, Zasedanje, Zapis
from dz.models import Oseba, Stranka

class Importer():

    def parse_time(self, time_string):
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

    def do_database_import(self, file_directory):
            files = os.listdir(file_directory)
            Seja.objects.all().delete()
            Zasedanje.objects.all().delete()
            Zapis.objects.all().delete()
            govorci_fn = os.path.join(os.path.dirname(__file__), 'govorci.json')
            govorci_map = json.load(open(govorci_fn))

            for file in sorted(files):
                print file, "..."
                counter = 0
                for fileData in open(os.path.join(file_directory, file), 'r'):
                    counter = counter + 1
                    print counter, ".."
                    # Parse JSON data and create models
                    jsonData = json.loads(fileData.replace("\\\\", "\\"))
                    with transaction.commit_on_success():
                        seja = Seja()
                        seja.mandat = int(jsonData.get('mandat'))
                        naslov_seje = jsonData.get('naslov')
                        if naslov_seje.startswith('0.  seja'):
                            continue # foo data
                        seja.naslov = naslov_seje
                        match = re.search('(\d+)\.\s*(redna|izredna)', naslov_seje, re.I)
                        if not match:
                            print naslov_seje
                        seja_slug = ('%s-%s' % match.groups()).lower()
                        seja.slug = seja_slug
                        seja.seja = jsonData.get('seja')
                        seja.url = jsonData.get('url')
                        seja.save()

                        # jsonSeja objects
                        for jsonSeja in jsonData.get('seja_info'):
                            sejaInfo = SejaInfo()
                            sejaInfo.seja = seja
                            sejaInfo.url = jsonSeja.get('url')
                            sejaInfo.naslov = jsonSeja.get('naslov')
                            sejaInfo.datum = dateutil.parser.parse(jsonSeja.get('datum'), dayfirst=True)
                            sejaInfo.save()

                        # Zasedanja
                        for jsonZasedanje in jsonData.get('zasedanja'):
                            for jsonPovezava in jsonZasedanje.get('povezave'):
                                zasedanje = Zasedanje()
                                zasedanje.datum = dateutil.parser.parse(jsonZasedanje.get('datum'), dayfirst=True)
                                zasedanje.seja = seja

                                if jsonPovezava.get('zacetek'):
                                    zasedanje.zacetek = self.parse_time(jsonPovezava.get('zacetek'))
                                if jsonPovezava.get('konec'):
                                    zasedanje.konec = self.parse_time(jsonPovezava.get('konec'))

                                zasedanje.tip = jsonPovezava.get('tip')
                                zasedanje.naslov = jsonPovezava.get('naslov')
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
                                        oseba_id = govorci_map.get(govorec, None)
                                        values.extend([
                                            count,
                                            zasedanje.id,
                                            govorec,
                                            oseba_id,
                                            '\n'.join(jsonZapis.get('odstavki'))
                                            ])
                                        count += 1
                                
                                params = values
                                onerowtempl = '(' + ', '.join(['%s']*len(keys)) + ')'
                                all_rows_template = ', '.join([onerowtempl]*(len(params)/len(keys)))
                                sql = '''INSERT INTO %s (%s) VALUES %s''' % (
                                    Zapis._meta.db_table,
                                    ', '.join(keys),
                                    all_rows_template)
                                if params:
                                    cursor.execute(sql, params)
        

    def do_solr_import(self):
        # Shrani zapise v Solr
        solr = sunburnt.SolrInterface(settings.SOLR_URL)
        solr.delete_all()       # Clear Solr index

        midnight = datetime.time(0, 0)
        numZapis = Zapis.objects.count()
        counter = 0

        for oseba in Oseba.objects.all():
            stranke = []
            for clan in oseba.clanstranke_set.all():
                if clan.stranka:
                    stranke.append((clan.stranka.ime, clan.stranka.okrajsava))
            dict = { "id" : "OS%d" % oseba.pk,
                     "tip":"oseba",
                     "ime" : "%s %s" % (oseba.ime, oseba.priimek),
                     "besedilo" : "%s %s %s %s" % (oseba.ime, oseba.priimek, oseba.email, " ".join([ime + " " + okrajsava for ime, okrajsava in stranke])) }
            solr.add(dict)

        print "Osebe imported, starting Stranke..."
        for stranka in Stranka.objects.all():
            imena_clanov = []
            for clan in stranka.clanstranke_set.all():
                imena_clanov.append("%s %s" % (clan.oseba.ime, clan.oseba.priimek))

            dict = { "id" : "ST%d" % stranka.pk,
                     "tip" : "stranka",
                     "ime" : "%s (%s)" % (stranka.ime, stranka.okrajsava),
                     "besedilo" : "%s %s %s %s %s" % (stranka.ime, stranka.okrajsava, stranka.email, stranka.maticna, " ".join(imena_clanov))}
            solr.add(dict)

        print "Stranked imported, starting Zapisi..."
        zasedanja = {}
        for zapis in Zapis.objects.select_related().all():
            zasedanje_id = zapis.zasedanje.pk
            dict = { "id": "ZP%d" % zapis.pk,
                     "tip": "zapis",
                     "zasedanje_id": zasedanje_id,
                     "seja_id": zapis.zasedanje.seja.pk,
                     "datum": datetime.datetime.combine(zapis.zasedanje.datum, midnight),    # Sunburnt expects datetime
                     "govorec":zapis.govorec,
                     "ime": zapis.zasedanje.seja.naslov,
                     "besedilo" : zapis.odstavki }
            solr.add(dict)


            if not zasedanja.has_key(zasedanje_id):
                zasedanja[zasedanje_id] = []
            zasedanja[zasedanje_id].append("%s: %s" % (zapis.govorec, zapis.odstavki))

            counter += 1
            if counter % 100 == 0:
                print counter,"/",numZapis

        print "Zapisi imported, starting Zasedanje..."
        counter = 0
        for zasedanje_id in zasedanja:
            zasedanje = Zasedanje.objects.get(pk=zasedanje_id)
            dict = { "id": "ZS%d" % zasedanje.pk,
                     "tip": "zasedanje",
                     "seja_id": zasedanje.seja.pk,
                     "datum": datetime.datetime.combine(zasedanje.datum, midnight),
                     "ime": zasedanje.seja.naslov,
                     "besedilo": "\n".join(zasedanja[zasedanje_id]) }
            solr.add(dict)
            zasedanja[zasedanje_id] = None
            counter += 1
            if counter % 100 == 0:
                print counter,"/", len(zasedanja)

        solr.commit()
        print "Data commited to Solr."
