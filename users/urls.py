from django.urls import path

from . import views


app_name = "users"

# This view is now used anymore
urlpatterns = [
    path("signup/", views.SignupPageView.as_view(), name="signup"),
]
