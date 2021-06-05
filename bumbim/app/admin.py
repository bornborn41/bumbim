from django.contrib import admin
from .models import Author, Post

# from .models import QuillPost


class PostAdmin(admin.ModelAdmin):

    list_display = ('id',  'author','title' ,'content','image',  'date_posted')
    list_display_links = ('id', 'author',)
    list_filter = ('author', 'date_posted')
    list_editable = ( 'title' ,'content','image', )
    search_fields = ( 'title','content' ,'author__username',)
    list_per_page = 20


admin.site.register(Post, PostAdmin)

class AuthorAdmin(admin.ModelAdmin):

    list_display = ('id',  'username','first_name' ,'last_name','image')
    list_display_links = ('id', 'username',)
    list_per_page = 20

admin.site.register(Author, AuthorAdmin)