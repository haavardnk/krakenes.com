from django.shortcuts import render, get_object_or_404, redirect
from posts.models import BlogPost, Comment, Tag, Category
from projects.models import Project
from django.core.paginator import Paginator
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.contrib.auth.models import User


def home(request):
    posts = BlogPost.objects.all().order_by('-id')
    return render(request, 'blog/home.html', {'posts': posts})


def blog(request):
    all_posts = BlogPost.objects.all().order_by('-id')

    if request.method == "POST":
        search_vector = SearchVector(
            'author__username', 'category__name', 'title', 'tags__name', 'content')
        post_list = BlogPost.objects.all().annotate(search=search_vector).filter(
            search=request.POST['search']).order_by('title', '-id').distinct('title')
    else:
        post_list = all_posts

    paginator = Paginator(post_list, 4)
    tags = Tag.objects.all()
    categories = Category.objects.all().annotate(posts_count=Count('blogpost'))

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    # Search for blog post
    if request.method == "POST":
        # If result:
        if post_list:
            return render(request, 'blog/blog.html', {
                'posts': posts,
                'all_posts': all_posts,
                'range': range(posts.paginator.num_pages+1),
                'tags': tags,
                'categories': categories,
                'message': 'Search results for ' + "'"+request.POST['search']+"':"
            })
        # If no result:
        return render(request, 'blog/blog.html', {
            'posts': posts,
            'all_posts': all_posts,
            'range': range(posts.paginator.num_pages+1),
            'tags': tags,
            'categories': categories,
            'message': 'There are no results that match your search.'
        })
    # No search:
    return render(request, 'blog/blog.html', {
        'posts': posts,
        'all_posts': all_posts,
        'range': range(posts.paginator.num_pages+1),
        'tags': tags,
        'categories': categories
    })


def post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    posts = BlogPost.objects.all().order_by('-id')
    tags = Tag.objects.all()
    categories = Category.objects.all().annotate(posts_count=Count('blogpost'))

    hit_count = HitCount.objects.get_for_object(post)
    HitCountMixin.hit_count(request, hit_count)

    if request.method == "POST":
        if request.user.is_authenticated:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                text=request.POST['comment'],
            )
            message = "Comment submitted."
            comment.save()

        return render(request, 'blog/post.html', {'post': post, 'posts': posts, 'tags': tags, 'categories': categories, 'message': message})

    return render(request, 'blog/post.html', {'post': post, 'posts': posts, 'tags': tags, 'categories': categories})
