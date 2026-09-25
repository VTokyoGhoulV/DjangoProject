from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from blog.form import PostForm
from blog.models import Blog


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = "post_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views += 1
        if post.views == 100:
            send_mail(
                subject="Статья достигла 100 просмотров",
                message=f'Статья "{post.title}" набрала 100 просмотров!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_RECIPIENT],
                fail_silently=False,
            )

        post.save(update_fields=["views"])
        return post

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm("blog.change_blog"):
            return queryset

        return queryset.filter(published=True)


class PostListView(LoginRequiredMixin, ListView):
    model = Blog
    queryset = Blog.objects.order_by("-date", "-pk")
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.request.user.has_perm("blog.change_blog"):
            return queryset

        return queryset.filter(published=True)


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    template_name = "post_create.html"
    context_object_name = "post"
    form_class = PostForm
    success_url = reverse_lazy("posts_list")
    permission_required = "blog.add_blog"


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    template_name = "post_update.html"
    context_object_name = "post"
    form_class = PostForm
    permission_required = "blog.change_blog"

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    template_name = "post_delete.html"
    success_url = reverse_lazy("posts_list")
    context_object_name = "post"
    permission_required = "blog.delete_blog"


class PostUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "blog.can_unpublish_blog"

    def post(self, request, pk):
        post = get_object_or_404(Blog, pk=pk)
        post.published = False
        post.save()

        return redirect("posts_list")
