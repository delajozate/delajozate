from django.contrib import admin
from delajozate.dz.models import Oseba, Stranka, Skupina, ClanStranke, \
	Mandat, Funkcija, Odbor, ClanOdbora

class FunkcijaAdmin(admin.ModelAdmin):
	list_display = ('oseba', 'mandat', 'od', 'do', 'podatki_preverjeni')
	list_filter = ('mandat', 'podatki_preverjeni')

class StrankaAdmin(admin.ModelAdmin):
	list_display = ('ime', 'okrajsava', 'twitter', 'od', 'do', 'podatki_preverjeni')

class OdborAdmin(admin.ModelAdmin):
	list_display = ('ime', 'mandat', 'od', 'do', 'podatki_preverjeni')

class ClanOdboraAdmin(admin.ModelAdmin):
	list_display = ('poslanec', 'odbor', 'od', 'do', 'podatki_preverjeni')

class OsebaAdmin(admin.ModelAdmin):
	list_display = ('ime', 'priimek', 'rojstni_dan', 'podatki_preverjeni', 'twitter', 'spletna_stran', 'slika')
	search_fields = ('ime', 'priimek')

class MandatAdmin(admin.ModelAdmin):
	list_display = ('st', 'od', 'do')

admin.site.register(Oseba, OsebaAdmin)
admin.site.register(Stranka, StrankaAdmin)
admin.site.register(Skupina)
admin.site.register(ClanStranke)
admin.site.register(Mandat, MandatAdmin)
admin.site.register(Funkcija, FunkcijaAdmin)
admin.site.register(Odbor, OdborAdmin)
admin.site.register(ClanOdbora, ClanOdboraAdmin)


