from django.shortcuts import render, redirect

from blog.forms import CreateBlogPostModelForm, UpdateBlogPostModelForm
from blog.models import BlogPost, BlogPostCover


def not_found(request):
    return render(request, '404.html')

def blog_post_list(request):
    blogs = BlogPost.objects.filter(deleted=False).order_by('-id')
    return render(request, template_name='blog_list.html', context={'blogs': blogs})


def blog_post_detail(request, pk):
    blog = BlogPost.objects.filter(id=pk).first()
    if not blog:
        return redirect('not_found')
    return render(request, template_name='blog_detail.html', context={'blog': blog})


def blog_create(request):
    if request.method == 'POST':
        form = CreateBlogPostModelForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            cover = form.cleaned_data['cover']
            BlogPostCover.objects.create(blog_post=blog, image=cover)
            return redirect('blog_list')
    else:
        form = CreateBlogPostModelForm()

    return render(request, template_name='blog_create.html', context={'form': form})


def blog_update(request, pk):
    blog = BlogPost.objects.filter(id=pk).first()
    if not blog:
        return redirect('not_found')

    if request.method == 'POST':
        form = UpdateBlogPostModelForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', pk=blog.pk)  # Redirect to the detail page
    else:
        form = UpdateBlogPostModelForm(instance=blog)  # Pre-fill the form with existing data

    return render(request, template_name='blog_update.html', context={'form': form})

def blog_delete(request, pk):
    blog = BlogPost.objects.filter(id=pk).first()
    if not blog:
        return redirect('not_found')

    if request.method == 'POST':
        blog.deleted = True
        blog.save()
        return redirect('blog_list')

    return render(request, template_name='blog_confirm_delete.html', context={'blog': blog})
