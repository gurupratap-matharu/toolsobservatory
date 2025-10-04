from django.urls import path

from tools.views import HomePageView

from . import views


app_name = "pages"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("about/", views.AboutPageView.as_view(), name="about"),
    path("terms/", views.TermsPageView.as_view(), name="terms"),
    path("privacy/", views.PrivacyPageView.as_view(), name="privacy"),
    path("contact/", views.ContactPageView.as_view(), name="contact"),
    path("robots.txt", views.RobotsView.as_view(), name="robots"),
    path("favicon.ico", views.favicon, name="favicon"),
]
