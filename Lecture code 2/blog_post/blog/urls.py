from django.urls import path
from blog.views import (
    not_found,
    blog_post_list,
    blog_post_detail,
    blog_create,
    blog_update,
    blog_delete
)
from blog.class_views import (
    BlogPostyListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView
)

urlpatterns = [
    path('not_found', not_found, name='not_found'),
    path('blog_list/', blog_post_list, name='blog_list'),
    path('blog_detail/<int:pk>/', blog_post_detail, name='blog_detail'),
    path('blog_create/', blog_create, name='blog_create'),
    path('blog_update/<int:pk>/', blog_update, name='blog_update'),
    path('blog_delete/<int:pk>/', blog_delete, name='blog_delete'),
    path('class_blog_list/', BlogPostyListView.as_view(), name='class_blog_list'),
    path('class_blog_detail/<int:pk>/', BlogPostDetailView.as_view(), name='class_blog_detail'),
    path('class_blog_create/', BlogPostCreateView.as_view(), name='class_blog_create'),
    path('class_blog_update/<int:pk>/', BlogPostUpdateView.as_view(), name='class_blog_update'),
    path('class_blog_delete/<int:pk>/', BlogPostDeleteView.as_view(), name='class_blog_delete'),
]
