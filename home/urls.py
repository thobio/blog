from django.urls import path
from .views import BlogView, PublicBlogView

urlpatterns = [
    path("blog/", BlogView.as_view()),
    path("allBlog/", PublicBlogView.as_view()),
]
