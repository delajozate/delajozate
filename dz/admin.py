from django.contrib import admin
from django.contrib.contenttypes import generic
from delajozate.dz.models import Oseba, Stranka, Skupina, ClanStranke, \
	Mandat, Funkcija, Odbor, ClanOdbora, ImeStranke, Pozicija

class FunkcijaAdmin(admin.ModelAdmin):
	search_fields = ('oseba__ime', 'oseba__priimek', 'funkcija')
	list_display = ('oseba', 'mandat', 'funkcija', 'od', 'do', 'podatki_preverjeni')
	list_filter = ('mandat', 'podatki_preverjeni')

class PozicijaInline(generic.GenericStackedInline):
	model = Pozicija
	ct_field = 'tip_organizacije'
	ct_fk_field = 'id_organizacije'
	extra = 1

class StrankaAdmin(admin.ModelAdmin):
	list_display = ('ime', 'okrajsava', 'twitter', 'od', 'do', 'podatki_preverjeni')

class OdborAdmin(admin.ModelAdmin):
	list_display = ('ime', 'mandat', 'od', 'do', 'podatki_preverjeni')

class ClanOdboraAdmin(admin.ModelAdmin):
	list_display = ('poslanec', 'odbor', 'od', 'do', 'podatki_preverjeni')
	inlines = [
		PozicijaInline,
	]

class OsebaAdmin(admin.ModelAdmin):
	list_display = ('ime', 'priimek', 'rojstni_dan', 'podatki_preverjeni', 'twitter', 'spletna_stran', 'slika')
	search_fields = ('ime', 'priimek')

class ClanStrankeAdmin(admin.ModelAdmin):
	search_fields = ('oseba__ime', 'oseba__priimek', 'stranka__ime')
	list_display = ('oseba', 'stranka', 'od', 'do', 'podatki_preverjeni')
	list_filter = ('podatki_preverjeni',)
	inlines = [
		PozicijaInline,
	]

class MandatAdmin(admin.ModelAdmin):
	list_display = ('st', 'od', 'do')

class ImeStrankeAdmin(admin.ModelAdmin):
	list_display = ('ime', 'od', 'do')

class PozicijaAdmin(admin.ModelAdmin):
	list_display = ('oseba', 'organizacija')

admin.site.register(Oseba, OsebaAdmin)
admin.site.register(Stranka, StrankaAdmin)
admin.site.register(Skupina)
admin.site.register(ClanStranke, ClanStrankeAdmin)
admin.site.register(Mandat, MandatAdmin)
admin.site.register(Funkcija, FunkcijaAdmin)
admin.site.register(Odbor, OdborAdmin)
admin.site.register(ClanOdbora, ClanOdboraAdmin)
admin.site.register(ImeStranke, ImeStrankeAdmin)
admin.site.register(Pozicija, PozicijaAdmin)
