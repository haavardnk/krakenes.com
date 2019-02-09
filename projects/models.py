from django.db import models
from django.contrib.auth.models import User
from posts.models import Category, Tag
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

class Project(models.Model, HitCountMixin):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField()
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    search_fields = ['title', 'category']

    def __str__(self):
        return self.title
        
    def summary(self):
        return self.content[:100] + "..."
    
    def pub_date_pretty(self):
        return self.pub_date.strftime('%e %b | %Y')
