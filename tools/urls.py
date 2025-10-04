from django.urls import path

from . import views


app_name = "tools"

urlpatterns = [
    path("", views.ToolListView.as_view(), name="tool-list"),
    path("search/", views.tool_search, name="tool-search"),
    path("tag/<slug:tag_slug>/", views.ToolListView.as_view(), name="tool-list-by-tag"),
    path("category/<slug:category_slug>/", views.ToolListView.as_view(), name="tool-list-by-category"),
    path("<slug:tool_slug>/", views.ToolDetailView.as_view(), name="tool-detail"),
    path("<slug:tool_slug>/report/", views.ToolErrorView.as_view(), name="tool-error"),
]
