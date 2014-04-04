import collections
import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView

import dz.news
from dz.models import Stranka, Oseba, Mandat, Tweet, Pozicija
from magnetogrami.models import Zasedanje, Glas, Glasovanje

from temporal import END_OF_TIME


def home(request):
    context = {
        'zasedanja': Zasedanje.objects.all().select_related('seja').order_by('-datum')[:15],
        'glasovanja': Glasovanje.objects.all().order_by('-datum')[:15],
    }
    return render(request, 'home.html', context)

class PoslanciList(ListView):
    model = Pozicija
    template_name = 'poslanci.html'
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        self.mandat_obj = None
        if self.mandat == 'danes':
            return Pozicija.objects.filter(
                tip='poslanec', do=END_OF_TIME).order_by('oseba')
        else:
            mandat = self.mandat[:-len('-mandat')]
            self.mandat_obj = get_object_or_404(Mandat, st=mandat)
            return Pozicija.objects.filter(
                tip='poslanec', organizacija__drzavnizbor__mandat=self.mandat_obj).order_by(
                    'od', 'oseba')

    def get_context_data(self, **kwargs):
        today = datetime.date.today()
        context = super(PoslanciList, self).get_context_data(**kwargs)

        mandati = Mandat.objects.all().values("st", "od", "do")
        for mandat in mandati:
            if mandat['do'] > today:
                mandat['do'] = None
        context['mandati'] = mandati
        if self.mandat == "danes":
            context['mandat'] = 'today'
        else:
            context['mandat'] = self.mandat
        context['mandat_obj'] = self.mandat_obj
        context['poslanci'] = context['object_list']
        return context

    def dispatch(self, request, mandat):
        self.mandat = mandat
        return super(PoslanciList, self).dispatch(request, mandat)

def d_squared(tracks, nodepairs):
    #for a,b in nodepairs:
        #(tracks[a]-tracks[b])**2

    return list(sorted([((tracks[a] - tracks[b]) ** 2, a, b) for a, b in nodepairs], reverse=True))


def stranke_json(request):
    "json strank za d3.js vizualizacijo"

    stiki = {}

    for s in Stranka.objects.all().order_by('od'):
        start_sticisce = stiki.setdefault(s.od, {})
        start_sticisce.setdefault('od', []).append(s)
        end_sticisce = stiki.setdefault(s.do, {})
        end_sticisce.setdefault('do', []).append(s)

    masters = {}
    steze = {}
    povezave = {}
    stiki_list = list(sorted(stiki.items()))
    for k, s in stiki_list:
        if len(s.get('od', [])) == 1 and len(s.get('do', [])) == 1:
            # preimenovanje
            s_v = s['od'][0]
            s_iz = s['do'][0]
            mastr = masters.setdefault(s_iz.id, s_iz.id)
            while mastr != masters[mastr]:
                mastr = masters[mastr]
            masters[s_v.id] = mastr
            steze.setdefault(mastr, [s_iz]).append(s_v)
        elif len(s.get('od', [])) + len(s.get('do', [])) > 2:
            for d in s.get('od', []):
                do = povezave.setdefault(d.id, [])
                do.extend([i.id for i in s.get('do', [])])

    for s in Stranka.objects.all().order_by('od'):
        if not s.id in masters:
            steza = masters.setdefault(s.id, s.id)
            steze.setdefault(steza, [s])

    povezave_resolved = []
    for k, v in povezave.items():
        for i in v:
            povezave_resolved.append((masters[k], masters[i]))

    steze_index = dict([(b, a) for a, b in list(enumerate(steze.keys()))])

    stranke = {}
    for s in Stranka.objects.all():
        s_dict = {
            'id': s.id,
            'od': (s.od.year, s.od.month, s.od.day),
            'do': (s.do.year, s.do.month, s.do.day),
            'ime': s.ime,
            'okrajsava': s.okrajsava,
            'barva': s.barva,
            'nastala_iz': [i.id for i in s.nastala_iz.all()],
            'spremenila_v': [v.id for v in s.spremenila_v.all()],
            }
        stranke[s.id] = s_dict

    condensed = {}
    for master_id, steza in steze.iteritems():
        newsteza = []
        for s in steza:
            s_dict = {
            'id': s.id,
            'od': (s.od.year, s.od.month, s.od.day),
            'do': (s.do.year, s.do.month, s.do.day),
            'ime': s.ime,
            'okrajsava': s.okrajsava,
            'barva': s.barva,
            'nastala_iz': [i.id for i in s.nastala_iz.all()],
            'spremenila_v': [v.id for v in s.spremenila_v.all()],
            }
            newsteza.append(s_dict)
        condensed[master_id] = newsteza

    return HttpResponse(json.dumps({'stranke_all': stranke, 'stranke_condensed': condensed}, indent=3), mimetype='application/json')

def pobarvaj_glasove(glasovi):
    classes = {
        #'Ni': 'yellow',
        'Za': 'green',
        'Proti': 'red',
    }
    for glas in glasovi:
        glas.cls = classes.get(glas.glasoval, "")
    return glasovi


def poslanec(request, slug):
    vote_limit = 15

    oseba = get_object_or_404(Oseba, slug=slug)
    glasovi = Glas.objects.filter(oseba=oseba).select_related(
        'glasovanje', 'glasovanje__seja').order_by(
            '-glasovanje__datum')[:vote_limit]

    '''
    tweeti = Tweet.objects.filter(oseba=oseba)
    '''
    pobarvaj_glasove(glasovi)

    context = {
        'oseba': oseba,
        'votes': glasovi,
    }

    return render(request, "poslanec.html", context)


class GlasovanjaList(ListView):
    model = Glas
    template_name = 'poslanec_glasovanja.html'
    paginate_by = 30
    limit = None

    # TODO: Dodaj filtre: zadnji teden, mesec, leto, mandat?

    def get_queryset(self, *args, **kwargs):
        qs = Glas.objects.filter(oseba=self.oseba).select_related(
            'glasovanje', 'glasovanje__seja').order_by( '-glasovanje__datum')
        if self.limit == 'letos':
            today = datetime.date.today()
            start = datetime.date(today.year, 1, 1)
            qs = qs.filter(glasovanje__datum__gte=start)
        return qs

    def get_context_data(self, **kwargs):
        context = super(GlasovanjaList, self).get_context_data(**kwargs)
        context['oseba'] = self.oseba
        context['votes'] = context['object_list']
        pobarvaj_glasove(context['votes'])
        return context

    def dispatch(self, request, slug):
        self.oseba = Oseba.objects.get(slug=slug)
        self.limit = request.GET.get('limit', None)
        return super(GlasovanjaList, self).dispatch(request, slug)


class TweetList(ListView):
    model = Tweet
    template_name = 'poslanec_tweet.html'
    paginate_by = 30

    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.filter(oseba=self.oseba).order_by('-created_at')
        return qs

    def get_context_data(self, **kwargs):
        context = super(TweetList, self).get_context_data(**kwargs)
        context['oseba'] = self.oseba
        context['tweets'] = context['object_list']
        return context

    def dispatch(self, request, slug):
        self.oseba = Oseba.objects.get(slug=slug)
        return super(TweetList, self).dispatch(request, slug)


def robots(request):

    robots_txt = """User-agent: *
Disallow: /iskanje/
"""

    return HttpResponse(robots_txt, mimetype="text/plain")
