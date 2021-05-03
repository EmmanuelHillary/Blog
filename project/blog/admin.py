from django.contrib import admin
from .models import Post, Profile, PostImage, Comment


class PostImageAdmin(admin.StackedInline):
    model = PostImage


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'status', 'created']
    list_filter = ['status', 'updated', 'created']
    search_fields = ('title', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    date_hierarchy = 'created'
    inlines = [PostImageAdmin]

    class Meta:
        model = Post


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'dob', 'photo']


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
