from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from blog.form import PostForm
from blog.models import Blog


class PostDetailView(DetailView):
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


class PostListView(ListView):
    model = Blog
    queryset = Blog.objects.filter(
        published=True
    ).order_by("-date", "-pk")
    template_name = "post_list.html"
    context_object_name = "posts"
    paginate_by = 6


class PostCreateView(CreateView):
    model = Blog
    template_name = "post_create.html"
    context_object_name = "post"
    form_class = PostForm
    success_url = reverse_lazy("posts_list")


class PostUpdateView(UpdateView):
    model = Blog
    template_name = "post_update.html"
    context_object_name = "post"
    form_class = PostForm

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.pk})



class PostDeleteView(DeleteView):
    model = Blog
    template_name = "post_delete.html"
    success_url = reverse_lazy("posts_list")
    context_object_name = "post"
