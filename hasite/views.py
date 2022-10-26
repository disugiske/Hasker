from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.db.models import Q
from django.http import HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from hasite.forms import UserRegisterForm, AddPost, AddCommentForm, Tags, UserUpdateForm, ProfileUpdateForm
from hasite.logic.vote import vote_func, get_vote_db
from hasite.models import Post, PostTags
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
        if search:
            # search_result = SearchQuery(search, search_type='websearch')
            search_result = Post.objects.filter(
                Q(title__icontains=search) | Q(text__icontains=search)).prefetch_related('tags', 'comments',
                                                                                         'author').select_related()
            return render(request, "index.html", {"posts": search_result[:20],
                                                  "trend": search_result[:20]})
        if tag:
            search_result = Post.objects.prefetch_related('tags', 'comments', 'author').select_related()
            search_tag = search_result.filter(
                Q(tags__post_tag__icontains=tag))
            html = render_to_string("indexjs.html", {"posts": search_tag[:20],
                                                     "trend": search_result[:20]})
            return JsonResponse(html, safe=False)
        # post_name = Post.objects.select_related('author').all()
        # post = post_name.annotate(search=SearchVector('title', 'text')).filter(search=search_result)


def auth(request: HttpRequest):
    if request.user.username != "":
        return redirect('hasker:index')
    if request.method == 'POST':
        return render(request, "user/auth.html")


def register(request):
    if request.user.username != "":
        return redirect('hasker:index')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            return redirect('hasker:index')
    else:
        form = UserRegisterForm()
    return render(request, 'user/registration.html', {'form': form})


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
    post = get_object_or_404(Post, id=pk)
    comments = post.comments.all().select_related()
    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_author_id = request.user.id
            comment.post_id = pk
            comment.save()
            return redirect(request.path)
    else:
        form = AddCommentForm()
    return render(request, 'post.html', {"comments": comments, "post": post, "form": form})


@login_required
def vote_comment(request):
    if request.method == "POST":
        up = request.POST.get("up")
        down = request.POST.get("down")
        vote_id = request.POST.get("vote_id")
        method = request.POST.get("method")
        try:
            vote, create, kind = get_vote_db(method, vote_id, request)
            print(vote, create, kind)
            json_resp = vote_func(vote, create, up, down, kind)
            return JsonResponse(json_resp)
        except Exception as e:
            print(e)
            return JsonResponse({"rating": "500"})


@login_required
def profile(request, name):
    user_profile = get_object_or_404(User.objects.select_related(), username=name)
    post = user_profile.post.all()
    for i in user_profile.post.all():
        print(i.title)
    return render(request, 'profile.html', {"user_profile": user_profile, "post": post})


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
