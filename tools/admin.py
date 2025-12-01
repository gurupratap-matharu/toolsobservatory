from django.contrib import admin

from .models import Category, Tool


admin.site.empty_value_display = "(None)"
admin.site.site_header = "Tools Observatory"
admin.site.site_title = "Tools Observatory Portal"
admin.site.index_title = "Welcome to ToolsObservatory"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "publish", "status", "js_path"]
    list_filter = ["status", "created", "publish"]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "publish"
    ordering = ["status", "publish"]
    show_facets = admin.ShowFacets.ALWAYS
