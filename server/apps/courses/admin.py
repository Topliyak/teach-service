from django.contrib import admin
from . import models


class SectionInline(admin.TabularInline):
	model = models.Section


class PageInline(admin.TabularInline):
	model = models.Page


class CourseAdmin(admin.ModelAdmin):
	readonly_fields = ('author', )
	inlines = [SectionInline]

	def save_model(self, request, obj, form, change):
		if obj.author_id is None:
			obj.author = request.user

		obj.save()


class SectionAdmin(admin.ModelAdmin):
	list_display = ('pk', 'name', 'course')
	list_display_links = ('name',)
	inlines = [PageInline]


class PageAdmin(admin.ModelAdmin):
	list_display = ('pk', 'name', 'order', 'section_info')

	def section_info(self, obj):
		return f'Section: {obj.section.name} | Course: {obj.section.course.name}'


admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.Section, SectionAdmin)
admin.site.register(models.Page, PageAdmin)
