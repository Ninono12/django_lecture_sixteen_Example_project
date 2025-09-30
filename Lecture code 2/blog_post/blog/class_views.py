from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import CreateBlogPostModelForm
from blog.models import BlogPost, BlogPostCover


class BlogPostyListView(ListView):
    model = BlogPost
    template_name = 'class_blog_list.html'
    context_object_name = 'blogs'
    queryset = BlogPost.objects.filter(deleted=False).order_by('-id')
    # queryset = BlogPost.objects.filter(Q(deleted=False) | Q(is_active=True), title='Blog 1').order_by('-id')


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'class_blog_detail.html'
    context_object_name = 'blog'


class BlogPostCreateView(CreateView):
    model = BlogPost
    # fields = ['title', 'text', 'document', 'is_active', 'category', 'authors']
    template_name = 'class_blog_create.html'
    success_url = '/blog/class_blog_list/'
    form_class = CreateBlogPostModelForm

    def form_valid(self, form):
        response = super().form_valid(form)
        cover = form.cleaned_data.get('cover')
        if cover:
            BlogPostCover.objects.create(blog_post=self.object, image=cover)
        return response


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'text', 'document', 'is_active', 'category']
    template_name = 'class_blog_update.html'

    def get_success_url(self):
        return f'/blog/class_blog_detail/{self.object.id}/'


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'class_blog_confirm_delete.html'
    context_object_name = 'blog'

    def form_valid(self, form):
        self.object.deleted  = True
        self.object.save()
        return redirect('class_blog_list')
