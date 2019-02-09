from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
        name = models.CharField(max_length=32)
        class Meta:
                verbose_name_plural = "Categories"
        def __str__(self):
            return self.name

class Tag(models.Model):
        name = models.CharField(max_length=32)
        def __str__(self):
            return self.name

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField()
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    search_fields = ['title','byline','symbol']

    def __str__(self):
        return self.title
        
    def summary(self):
        return self.content[:100]
    
    def pub_date_pretty(self):
        return self.pub_date.strftime('%b %e %Y')

