from django.contrib import admin
import re
import datetime
from delajozate.magnetogrami.models import GovorecMap, Video, Zasedanje

class GovorecMapAdmin(admin.ModelAdmin):
	list_display = ('govorec', 'oseba')
	search_fields = ('govorec',)

class VideoAdmin(admin.ModelAdmin):
	list_display = ('title', 'zasedanje', 'datum', 'ava_id', 'url')
	list_filter = ('datum',)

	def get_queryset(self, request):
		qs = super(VideoAdmin, self).get_queryset(request)
		return qs.select_related('zasedanje', 'zasedanje__seja')
	
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "zasedanje":
			# filter zasedanja by datum
			m = re.search('/magnetogrami/video/(\d+)/$', request.path)
			v = Video.objects.get(pk=m.group(1))
			week = datetime.timedelta(7)
			kwargs['queryset'] = Zasedanje.objects.filter(datum__gte=v.datum - week, datum__lte=v.datum + week)
		return super(VideoAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(GovorecMap, GovorecMapAdmin)
admin.site.register(Video, VideoAdmin)
