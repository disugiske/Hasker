from django.contrib import admin
from hasite.models import (
    Post,
    PostComments,
    VoteCommentCount,
    VotePostCount,
    PostTags,
    Profile,
)


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "date_posted", "author", "votes", "id")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "comment_author", "rating", "id")


class CommentCount(admin.ModelAdmin):
    list_display = ("user", "comment", "comment_count")


class PostCount(admin.ModelAdmin):
    list_display = ("user", "post", "post_count")


class TagsAdmin(admin.ModelAdmin):
    list_display = ("post_tag", "post_id")


admin.site.register(Post, PostAdmin)
admin.site.register(PostComments, CommentAdmin)
admin.site.register(VoteCommentCount, CommentCount)
admin.site.register(VotePostCount, PostCount)
admin.site.register(PostTags, TagsAdmin)
admin.site.register(Profile)
