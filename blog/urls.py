from blog import views as blog

from django.urls import path

urlpatterns = [
    path("post_detail/<int:pk>/", blog.PostDetailView.as_view(), name="post_detail"),
    path("posts_list/", blog.PostListView.as_view(), name="posts_list"),
    path("add_post/", blog.PostCreateView.as_view(), name="add_post"),
    path("update_post/<int:pk>/", blog.PostUpdateView.as_view(), name="update_post"),
    path("delete_post/<int:pk>/", blog.PostDeleteView.as_view(), name="delete_post"),
]