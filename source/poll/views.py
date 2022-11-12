import asyncio
from statistics import mean
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Avg, Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from poll.forms import (
    AddPost,
    AddCommentForm,
    Tags,
)
from tasks.sender import send_email
from poll.utils import vote_func, get_vote_db
from poll.models import Post, PostTags, PostComments

from users.models import Profile

subject = {
    "registration": "Registration on hasker",
    "comment": "New answer on Husker",
}


def index(request: HttpRequest):
    post_name = Post.objects.prefetch_related(
        "tags", "comments", "author"
    ).select_related()
    trend = post_name.order_by("-votes")[:20]
    posts = post_name.order_by("-date_posted")[:20]
    return render(request, "index.html", {"posts": posts, "trend": trend})


def index_hot(request: HttpRequest):
    post_name = (
        Post.objects.order_by("-votes", "-date_posted")
            .prefetch_related("tags", "comments", "author")
            .all()
    )
    return render(
        request,
        "index.html",
        {"posts": post_name.select_related()[:20], "trend": post_name},
    )


@login_required
def search(request, tag=None, word=None):
    post = None
    if request.method == "POST":
        word = request.POST.get("word")
        tag = request.POST.get("tag")

    search_result = Post.objects.prefetch_related("tags", "comments", "author").select_related()
    trend = search_result.order_by("-votes")[:20]
    if tag:
        post = search_result.filter(Q(tags__post_tag__icontains=tag)).order_by("-votes", "-date_posted")[:20]
    if word:
        post = search_result.filter(Q(title__icontains=word) | Q(text__icontains=word)
                                    ).order_by("-votes", "-date_posted")[:20]

    if request.method == "GET":
        return render(request, "index.html", {"posts": post, "trend": trend, "search": tag or word})

    html = render_to_string(
        "indexjs.html",
        {
            "posts": post,
            "trend": trend,
            "search": tag or word,
        },
    )
    response = JsonResponse(html, safe=False)
    return response


@login_required()
def addpost(request):
    if request.method == "POST":
        form = AddPost(request.POST)
        tags = Tags(request.POST)
        if form.is_valid() and tags.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post_id = Post(id=post.pk)
            tag = tags.cleaned_data["post_tag"]
            create = []
            for i in tag.replace(" ", "").split(","):
                create.append(PostTags(post_tag=i, post_id=post_id))
            PostTags.objects.bulk_create(create)
            return redirect(f"/post/{post.pk}")
    else:
        form = AddPost()
        tags = Tags()
    return render(request, "addpost.html", {"form": form, "tags": tags})


@login_required
def post(request, pk):
    post = get_object_or_404(Post.objects.select_related(), id=pk)
    comments = post.comments.all().select_related()
    trends = Post.objects.order_by("-votes")[:20]
    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_author_id = request.user.id
            comment.post_id = pk
            comment.save()
            message = (
                f"Hi {request.user.username},"
                f" you have new answer to your question https://hasker.site/post/{post.id}"
            )
            asyncio.run(
                send_email(
                    message=message,
                    subject=subject["comment"],
                    email=request.user.email,
                )
            )
            return redirect(request.path)
    else:
        form = AddCommentForm()
    return render(
        request,
        "post.html",
        {
            "comments": comments.order_by("-best", "-rating")[:30],
            "post": post,
            "trends": trends,
            "form": form,
        },
    )


@login_required
def vote_comment(request):
    if request.method == "POST":
        up = request.POST.get("up")
        down = request.POST.get("down")
        vote_id = request.POST.get("vote_id")
        method = request.POST.get("method")
        vote, create, kind = get_vote_db(method, vote_id, request)
        json_resp = vote_func(vote, create, up, down, kind)
        return JsonResponse(json_resp)


@login_required
def best_choice(request):
    best_now = 0
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        best_comment = PostComments.objects.get(id=comment_id)
        if request.user != best_comment.post.author:
            return JsonResponse({}, status=403)
        try:
            best_now = PostComments.objects.get(post=best_comment.post, best=1)
            best_now.best = False
            best_now.save()
            best_now = best_now.id
        except ObjectDoesNotExist:
            pass
        best_comment.best = True
        best_comment.save()
        return JsonResponse({"best_old": best_now})


@login_required
def profile(request, name):
    user_profile = get_object_or_404(
        Profile.objects.prefetch_related(
            "post", "post__comments", "post__tags",
        ),
        username=name,
    )
    mean_rating = user_profile.post.aggregate(
        comments=Avg("comments__rating"), posts=Avg("votes")
    )
    comments = mean_rating.get("comments") if mean_rating.get("comments") else 0
    posts = mean_rating.get("posts") if mean_rating.get("posts") else 0
    rating = mean([comments, posts])

    comments_amount = user_profile.post.aggregate(Count("comments"))
    return render(
        request,
        "profile.html",
        {
            "user_profile": user_profile,
            "post": user_profile.post.order_by("-votes", "-date_posted")[
                    :20
                    ].prefetch_related("tags"),
            "mean": rating,
            "comments_amount": comments_amount["comments__count"],
        },
    )
