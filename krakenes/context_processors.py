from portfolio.models import Album
from posts.models import Category

def get_albums(request):
    albums = Album.objects.all()
    return {
        'albums': albums
    }

def get_categories(request):
    categories = Category.objects.all()
    return {
        'categories': categories
    }