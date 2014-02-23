from django.contrib import admin
from django.contrib.contenttypes import generic
from delajozate.dz.models import Oseba, Stranka, Skupina, \
	Mandat, DelovnoTelo, ImeStranke, Pozicija

class PozicijaInline(generic.GenericStackedInline):
	model = Pozicija
	ct_field = 'tip_organizacije'
	ct_fk_field = 'id_organizacije'
	extra = 1

class StrankaAdmin(admin.ModelAdmin):
	list_display = ('ime', 'okrajsava', 'twitter', 'od', 'do', 'podatki_preverjeni')

class DelovnoTeloAdmin(admin.ModelAdmin):
	list_display = ('ime', 'mandat', 'dz_id', 'od', 'do', 'podatki_preverjeni')

class OsebaAdmin(admin.ModelAdmin):
	list_display = ('ime', 'priimek', 'rojstni_dan', 'podatki_preverjeni', 'twitter', 'spletna_stran', 'slika')
	search_fields = ('ime', 'priimek')

class MandatAdmin(admin.ModelAdmin):
	list_display = ('st', 'od', 'do')

class ImeStrankeAdmin(admin.ModelAdmin):
	list_display = ('ime', 'od', 'do')

class PozicijaAdmin(admin.ModelAdmin):
	list_display = ('oseba', 'tip', 'organizacija')
	search_fields = ('oseba__ime', 'oseba__priimek',)

admin.site.register(Oseba, OsebaAdmin)
admin.site.register(Stranka, StrankaAdmin)
admin.site.register(Skupina)
admin.site.register(Mandat, MandatAdmin)
admin.site.register(DelovnoTelo, DelovnoTeloAdmin)
admin.site.register(ImeStranke, ImeStrankeAdmin)
admin.site.register(Pozicija, PozicijaAdmin)
