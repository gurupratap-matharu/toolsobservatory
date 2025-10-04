from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView
from taggit.models import Tag

from .forms import SearchForm, ToolErrorForm
from .models import Category, Tool


class HomePageView(ListView):
    """
    Simple view to render on the home page of our project.
    """

    model = Tool
    template_name = "tools/tool_home.html"
    context_object_name = "tools"


class ToolListView(ListView):
    model = Tool
    template_name = "tools/tool_list.html"
    context_object_name = "tools"

    def get_queryset(self):
        qs = Tool.published.all()

        tag_slug = self.kwargs.get("tag_slug")
        category_slug = self.kwargs.get("category_slug")

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            qs = qs.filter(tags__in=[tag])
            self.extra_context = {"tag": tag}

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            qs = qs.filter(category=category)
            self.extra_context = {"category": category}

        return qs


class ToolDetailView(DetailView):
    template_name = "tools/tool_detail.html"
    model = Tool
    slug_url_kwarg = "tool_slug"


def tool_search(request):
    form = SearchForm()
    query = request.GET.get("query", None)
    results = []

    if query:
        form = SearchForm(request.GET)
        results = Tool.published.filter(Q(name__icontains=query) | Q(body__icontains=query))
    else:
        results = []

    context = {
        "form": form,
        "query": query,
        "results": results,
    }

    return render(request, "tools/tool_search.html", context)


class ToolErrorView(SuccessMessageMixin, FormView):
    form_class = ToolErrorForm
    template_name = "tools/tool_error.html"
    success_message = "Message sent successfully"

    def get_object(self):
        tool_slug = self.kwargs.get("tool_slug")
        tool = get_object_or_404(Tool, slug=tool_slug, status=Tool.Status.PUBLISHED)
        return tool

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tool"] = self.get_object()
        return context

    def get_success_url(self):
        return reverse_lazy("tools:tool-list")

    def form_valid(self, form):
        form.tool = self.get_object()
        form.send_mail()
        return super().form_valid(form)
