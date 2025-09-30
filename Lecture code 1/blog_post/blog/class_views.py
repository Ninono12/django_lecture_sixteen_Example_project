from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogPostModelForm, UpdateBlogPostModelForm
from blog.models import BlogPost, BannerImage


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'class_blog_list.html'
    context_object_name = 'blog_posts'
    queryset = BlogPost.objects.filter(deleted=False)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'class_blog_detail.html'
    context_object_name = 'blog'


class BlogPostCreateView(CreateView):
    model = BlogPost
    # fields = ['title', 'text', 'active', 'document', 'category', 'authors']
    template_name = 'class_blog_create.html'
    success_url = '/blog/class_blog_post_list/'
    form_class = BlogPostModelForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        response = super().form_valid(form)
        banner_image = form.cleaned_data['banner_image']
        blog_post = self.object
        BannerImage.objects.create(blog_post=blog_post, image=banner_image)

        return response


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = UpdateBlogPostModelForm
    template_name = 'class_blog_update.html'

    def get_success_url(self):
        return reverse_lazy('class_blog_post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'class_blog_post_confirm_delete.html'
    success_url = reverse_lazy("class_blog_post_list")

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.deleted = True
        self.object.save()
        return redirect(self.success_url)
