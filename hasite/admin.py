from django.contrib import admin
from hasite.models import Post, PostComments, VoteCommentCount, VotePostCount

admin.site.register(Post)
admin.site.register(PostComments)
admin.site.register(VoteCommentCount)
admin.site.register(VotePostCount)
