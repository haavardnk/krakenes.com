from django.shortcuts import render, get_object_or_404, redirect
from posts.models import BlogPost, Comment, Tag, Category
from projects.models import Project
from django.core.paginator import Paginator
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.contrib.postgres.search import SearchVector
from django.db.models import Count

def home(request):
    posts = BlogPost.objects
    projects = Project.objects
    return render(request, 'blog/home.html', {'posts':posts, 'projects':projects})

def blog(request):
    post_list = BlogPost.objects.all()
    paginator = Paginator(post_list, 4)
    tags = Tag.objects.all()
    categories = Category.objects.all().annotate(posts_count=Count('blogpost'))

    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog/blog.html', {'posts':posts, 'range':range(posts.paginator.num_pages+1), 'tags':tags, 'categories':categories})

def post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    posts = BlogPost.objects.all()
    tags = Tag.objects.all()
    categories = Category.objects.all().annotate(posts_count=Count('blogpost'))

    if request.method == "POST":
        comment = Comment.objects.create(post=post, author = request.POST['username'], text=request.POST['comment'], email = request.POST['email'])
        comment.save()
        return render(request, 'blog/post.html', {'post':post})

    hit_count = HitCount.objects.get_for_object(post)
    HitCountMixin.hit_count(request, hit_count)

    return render(request, 'blog/post.html', {'post':post, 'posts':posts, 'tags':tags, 'categories':categories})

def search(request):
    if request.method == "POST":
        posts = BlogPost.objects.annotate(
            search=SearchVector('author', 'category', 'title', 'tags', 'content' )
        ).filter(search=request.POST('search')).all()
        return render(request, 'blog/blog.html', {'posts':posts})
    