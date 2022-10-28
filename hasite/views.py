import json
import time
from statistics import mean

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg, Count
from django.db.models.functions import Round
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from hasite.forms import UserRegisterForm, AddPost, AddCommentForm, Tags, UserUpdateForm, ProfileUpdateForm
from hasite.logic.vote import vote_func, get_vote_db
from hasite.models import Post, PostTags, PostComments
from django.contrib.auth.models import User


def index(request: HttpRequest):
    post_name = Post.objects.prefetch_related('tags', 'comments', 'author').select_related()
    trend = post_name.order_by('-votes')[:20]
    posts = post_name.order_by('-date_posted')[:20]
    return render(request, "index.html", {"posts": posts,
                                          "trend": trend})


def index_hot(request: HttpRequest):
    post_name = Post.objects.order_by('-votes').prefetch_related('tags', 'comments', 'author').all()
    return render(request, "index.html", {"posts": post_name.select_related()[:20], "trend": post_name})


def search(request):
    if request.method == "POST":
        search = request.POST.get("search")
        tag = request.POST.get("tag")
        search_result = Post.objects.prefetch_related('tags', 'comments', 'author').select_related()
        if tag:
            search_word = tag
            search_res = search_result.filter(Q(tags__post_tag__icontains=tag))
        if search:
            search_word = search
            search_res = search_result.filter(
                Q(title__icontains=search) | Q(text__icontains=search))
        html = render_to_string("indexjs.html", {"posts": search_res.order_by('-votes', '-date_posted')[:20],
                                                 "trend": search_result.order_by('-votes')[:20],
                                                 "search": search_word
                                                 })

        response = JsonResponse(html, safe=False)
        return response
        # return redirect('hasker:index')
        # return render(request, "index.html", {"posts": search_res.order_by('-votes', '-date_posted')[:20],
        #                                   "trend": search_result.order_by('-votes')[:20]})
        # post_name = Post.objects.select_related('author').all()
        # post = post_name.annotate(search=SearchVector('title', 'text')).filter(search=search_result)


def auth(request: HttpRequest):
    if request.method == 'POST':
        return render(request, "user/auth.html")


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        user_image = ProfileUpdateForm(request.POST,
                                       request.FILES)
        if form.is_valid() and user_image.is_valid():
            form.save()
            user_image.save(commit=False)
            user_image.instance.user = form.instance
            user_image.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('hasker:index')
    else:
        form = UserRegisterForm()
        user_image = ProfileUpdateForm()
    return render(request, 'user/registration.html', {'form': form, 'user_image': user_image})


@login_required(login_url="hasker:auth")
def addpost(request):
    if request.method == "POST":
        form = AddPost(request.POST)
        tags = Tags(request.POST)
        if form.is_valid() and tags.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            post_id = Post(id=post.pk)
            tag = tags.cleaned_data['post_tag']
            create = []
            for i in tag.replace(" ", "").split(","):
                create.append(PostTags(post_tag=i, post_id=post_id))
            PostTags.objects.bulk_create(create)
            return redirect(f'/post/{post.pk}')
    else:
        form = AddPost()
        tags = Tags()
    return render(request, 'addpost.html', {'form': form, 'tags': tags})


@login_required
def post(request, pk):
    post = get_object_or_404(Post.objects.select_related(), id=pk)
    comments = post.comments.all().select_related()
    trends = Post.objects.order_by('-votes')[:20]
    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_author_id = request.user.id
            comment.post_id = pk
            comment.save()
            time.sleep(0.1)
            return redirect(request.path)
    else:
        form = AddCommentForm()
    return render(request, 'post.html', {"comments": comments.order_by('-best', '-rating')[:30], "post": post,"trends":trends, "form": form})


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
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        best_comment = PostComments.objects.get(id=comment_id)
        best_now = PostComments.objects.get(best=1)
        if best_now:
            best_now.best = 0
            best_now.save()
        best_comment.best = 1
        best_comment.save()
        return JsonResponse({})


def profile(request, name):
    user_profile = get_object_or_404(User.objects.prefetch_related('post', 'post__comments', 'post__tags', 'profile'),
                                     username=name)
    mean_rating = user_profile.post.aggregate(comments=Avg('comments__rating'), posts=Avg('votes'))
    comments = (mean_rating.get("comments") if mean_rating.get("comments") else 0)
    posts = (mean_rating.get('posts') if mean_rating.get('posts') else 0)
    rating = mean([comments, posts])

    comments_amount = user_profile.post.aggregate(Count('comments'))
    return render(request, 'profile.html',
                  {"user_profile": user_profile,
                   "post": user_profile.post.order_by('-votes', '-date_posted')[:20].prefetch_related('tags'),
                   "mean": rating,
                   "comments_amount": comments_amount['comments__count']})


@login_required
def account(request):
    if request.method == 'POST':
        update_user = UserUpdateForm(request.POST, instance=request.user)
        update_profile = ProfileUpdateForm(request.POST,
                                           request.FILES,
                                           instance=request.user.profile)
        if update_profile.is_valid():
            update_profile.save()
            messages.success(request, f'Ваше фото успешно обновлено')
        if update_user.is_valid():
            update_user.save()
            messages.success(request, f'Ваш профиль успешно обновлен')
        return redirect('hasker:account')

    else:
        update_user = UserUpdateForm(instance=request.user)
        update_profile = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'user/account.html',
                  {"update_user": update_user,
                   "update_profile": update_profile})


def search_res(request):
    return request
