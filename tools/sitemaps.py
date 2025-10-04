from django.contrib.sitemaps import Sitemap

from .models import Tool


class ToolSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Tool.published.all()

    def lastmod(self, obj):
        return obj.updated
