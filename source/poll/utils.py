from django.core.mail import send_mail

from hasker import settings
from poll.models import VotePostCount, VoteCommentCount


def get_vote_db(method, vote_id, request):
    if method == "post_vote":
        vote, create = VotePostCount.objects.select_related().get_or_create(
            post_id=vote_id, user_id=request.user.id
        )
        return vote, create, "post"
    if method == "comment_vote":
        vote, create = VoteCommentCount.objects.select_related().get_or_create(
            comment_id=vote_id, user_id=request.user.id
        )
        return vote, create, "comment"


def counts(vote, kind, delta):
    if kind == "post":
        vote.post_count += delta
        vote.save()
        vote.post.votes += delta
        vote.post.save()
        return vote.post.votes
    if kind == "comment":
        vote.comment_count += delta
        vote.save()
        vote.comment.rating += delta
        vote.comment.save()
        return vote.comment.rating


def vote_func(vote, create, up, down, kind):
    if kind == "post":
        count_static = vote.post_count
    if kind == "comment":
        count_static = vote.comment_count
    if create:
        if up:
            return {"rating": counts(vote, kind, 1)}
        if down:
            return {"rating": counts(vote, kind, -1)}
    if vote:
        if up:
            if count_static + 1 > 1:
                return {"rating": "err"}
            else:
                return {"rating": counts(vote, kind, 1)}
        if down:
            if count_static - 1 < -1:
                return {"rating": "err"}
            else:
                return {"rating": counts(vote, kind, -1)}


def send_mail_comment(user, post_id):
    subject = "New answer on hasker"
    message = f"Hi {user.username}, you have new answer to your question https://hasker.site/post/{post_id}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, "disugiske@yandex.ru"]
    send_mail(subject, message, email_from, recipient_list)
