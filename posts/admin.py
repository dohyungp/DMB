from django.contrib import admin

# Register your models here.
from posts.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "timestamp"]
    list_display_links = ["updated"]
    list_editable = ["title"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["title","oontent"]
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)