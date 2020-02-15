from django.shortcuts import render, get_object_or_404, redirect
from posts.models import BlogPost, Comment, Tag, Category
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.contrib.auth.models import User


def home(request):
    all_posts = BlogPost.objects.all().order_by('-id')
    post_list = all_posts
    categories = Category.objects.all()

    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    return render(request, 'blog/home.html', {'posts': posts, 'categories': categories, 'range': range(posts.paginator.num_pages+1)})

def search(request):
    all_posts = BlogPost.objects.all().order_by('-id')

    if request.method == 'POST' and 'search' in request.POST:
        search_vector = SearchVector(
            'author__username', 'category__name', 'title', 'tags__name', 'content')
        post_list = BlogPost.objects.all().annotate(search=search_vector).filter(
            search=request.POST['search']).order_by('-id', 'title').distinct('id')
        search_string = request.POST['search']

    paginator = Paginator(post_list, 6)
    tags = Tag.objects.all()
    categories = Category.objects.all()


    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'blog/search.html', {
        'posts': posts,
        'all_posts': all_posts,
        'range': range(posts.paginator.num_pages+1),
        'tags': tags,
        'categories': categories,
        'search_string': search_string
    })


def post(request, post_slug):
    post = get_object_or_404(BlogPost, slug=post_slug)
    posts = BlogPost.objects.all().order_by('-id')
    tags = Tag.objects.all()
    categories = Category.objects.all().annotate(posts_count=Count('blogpost'))

    if request.method == "POST":
        if request.user.is_authenticated:
            comment = Comment.objects.create(
                post=post,
                author=request.user,
                text=request.POST['comment'],
            )
            selected_category = "Comment submitted."
            comment.save()

        return render(request, 'blog/post.html', {'post': post, 'posts': posts, 'tags': tags, 'categories': categories, 'selected_category': selected_category})

    return render(request, 'blog/post.html', {'post': post, 'posts': posts, 'tags': tags, 'categories': categories})

def category(request, category_name):
    category = get_object_or_404(Category, name=category_name)

    categories = Category.objects.all()
    post_list = BlogPost.objects.all().filter(category=category).order_by('-id').distinct('id')

    category_entries = len(post_list)

    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    return render(request, 'blog/category.html', {'posts': posts, 'category': category, 'categories':categories, 'category_entries':category_entries, 'range': range(posts.paginator.num_pages+1)})