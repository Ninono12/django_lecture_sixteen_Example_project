from django.urls import path
from blog.views import (
    not_found,
    blog_post_list,
    blog_post_detail,
    blog_post_create,
    blog_post_update,
    blog_post_delete
)
from blog.class_views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView
)

urlpatterns = [
    path('not_found/', not_found, name='not_found'),
    path('blog_post_list/', blog_post_list, name='blog_post_list'),
    path('blog_post_detail/<int:pk>/', blog_post_detail, name='blog_post_detail'),
    path('blog_post_create/', blog_post_create, name='blog_post_create'),
    path('blog_post_update/<int:pk>/', blog_post_update, name='blog_post_update'),
    path('blog_post_delete/<int:pk>/', blog_post_delete, name='blog_post_delete'),
    path('class_blog_post_list/', BlogPostListView.as_view(), name='class_blog_post_list'),
    path('class_blog_post_detail/<int:pk>/', BlogPostDetailView.as_view(), name='class_blog_post_detail'),
    path('class_blog_post_create/', BlogPostCreateView.as_view(), name='class_blog_post_create'),
    path('class_blog_post_update/<int:pk>/', BlogPostUpdateView.as_view(), name='class_blog_post_update'),
    path('class_blog_post_delete/<int:pk>/', BlogPostDeleteView.as_view(), name='class_blog_post_delete')

]
