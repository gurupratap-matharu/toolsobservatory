from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from blog.sitemaps import PostSitemap
from tools.sitemaps import ToolSitemap


sitemaps = {"posts": PostSitemap, "tools": ToolSitemap}


urlpatterns = [
    path("private/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("users.urls"), name="users"),
    path("blog/", include("blog.urls", namespace="blog")),
    path("tools/", include("tools.urls", namespace="tools")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include("pages.urls", namespace="pages")),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add routes to test error templates
    urlpatterns += [
        path("test404/", TemplateView.as_view(template_name="404.html")),
        path("test500/", TemplateView.as_view(template_name="500.html")),
        path("styleguide/", TemplateView.as_view(template_name="styleguide.html")),
    ]


if not settings.TESTING:
    urlpatterns = [*urlpatterns] + debug_toolbar_urls()
