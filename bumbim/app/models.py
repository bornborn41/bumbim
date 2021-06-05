from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from djrichtextfield.models import RichTextField

# Create your models here.
class Author(AbstractUser):
    description = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='profile_pics') 


    def __str__(self):
        return f'ID:{self.id} ({self.username})'
    
    class Meta:
        verbose_name = 'Author'


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(blank=True,null=True,upload_to='post_image')
    title = models.CharField(max_length=100)
    # content = models.TextField(blank=True,null=True)
    content = RichTextField()
    date_posted = models.DateTimeField(default=timezone.now)


    class Meta:
        ordering = ('-date_posted', )

    def __str__(self):
        return f' {self.title} ของ {self.author}' 

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})