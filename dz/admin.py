from django.contrib import admin
from delajozate.dz.models import Oseba, Stranka, Skupina, ClanStranke, \
	Mandat, Poslanec, Odbor, ClanOdbora

class PoslanecAdmin(admin.ModelAdmin):
	list_display = ('oseba', 'mandat', 'od', 'do')
	list_filter = ('mandat',)

admin.site.register(Oseba)
admin.site.register(Stranka)
admin.site.register(Skupina)
admin.site.register(ClanStranke)
admin.site.register(Mandat)
admin.site.register(Poslanec, PoslanecAdmin)
admin.site.register(Odbor)
admin.site.register(ClanOdbora)


