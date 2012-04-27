from django.contrib import admin

from delajozate.magnetogrami.models import GovorecMap

class GovorecMapAdmin(admin.ModelAdmin):
	list_display = ('govorec', 'oseba')

admin.site.register(GovorecMap, GovorecMapAdmin)