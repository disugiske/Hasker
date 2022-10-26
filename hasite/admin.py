from django.contrib import admin
from hasite.models import Post, PostComments, VoteCommentCount, VotePostCount

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'comment_author', 'rating')

class CommentCount(admin.ModelAdmin):
    list_display = ('user', 'comment', 'comment_count')

class PostCount(admin.ModelAdmin):
    list_display = ('user', 'post', 'post_count')

admin.site.register(Post, PostAdmin)
admin.site.register(PostComments, CommentAdmin)
admin.site.register(VoteCommentCount, CommentCount)
admin.site.register(VotePostCount, PostCount)
