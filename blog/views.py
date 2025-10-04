import logging

from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import FormView, ListView
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm, SearchForm
from .models import Post


logger = logging.getLogger(__name__)


class PostListView(ListView):
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post_list.html"

    def get_queryset(self):
        qs = Post.published.all()

        tag_slug = self.kwargs.get("tag_slug")
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            qs = qs.filter(tags__in=[tag])
            self.extra_context = {"tag": tag}

        return qs


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    comments = post.comments.filter(active=True)

    # Build similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by("-same_tags", "-publish")

    context = {"comments": comments, "post": post, "similar_posts": similar_posts}

    return render(request, "blog/post_detail.html", context)


class EmailPostView(SuccessMessageMixin, FormView):
    form_class = EmailPostForm
    template_name = "blog/post_share.html"
    success_message = "E-mail sent successfully"

    def get_object(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        return post

    def form_valid(self, form):
        post = self.get_object()
        post_url = self.request.build_absolute_uri(post.get_absolute_url())

        form.post = post
        form.post_url = post_url
        form.send_mail()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.get_object()
        return context

    def get_success_url(self):
        post = self.get_object()
        return post.get_absolute_url()


class CommentView(FormView):
    template_name = "blog/post_comment.html"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.get_object()
        return context

    def form_valid(self, form):
        post = self.get_object()
        form.instance.post = post
        form.save()
        return super().form_valid(form)

    def get_object(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        return post

    def get_success_url(self):
        post = self.get_object()
        return post.get_absolute_url()


def post_search(request):
    form = SearchForm()
    query = request.GET.get("query", None)
    results = []

    if query:
        form = SearchForm(request.GET)
        results = Post.published.filter(title__icontains=query)
    else:
        results = []

    context = {
        "form": form,
        "query": query,
        "results": results,
    }

    return render(request, "blog/post_search.html", context)
