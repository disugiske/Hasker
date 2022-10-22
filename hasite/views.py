from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from hasite.forms import UserRegisterForm, AddPost, AddCommentForm
from hasite.logic.vote import vote_func, get_vote_db
from hasite.models import Post, PostComments, VoteCommentCount, VotePostCount


# @login_required(login_url="hasker:auth")
def index(request: HttpRequest):
    post_name = Post.objects.select_related()
    if post_name is None:
        post_name = "none"
    # else:
    #     print(post_name.id)
    #     print(post_name.comments.filter(post_id=1))
    # return redirect('hasker:addpost')
    return render(request, "index.html", {"posts": post_name.all()})


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


def addpost(request):
    if request.method == "POST":
        form = AddPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            print(post.pk)
            return redirect('hasker:index')
    else:
        form = AddPost()
    return render(request, 'addpost.html', {'form': form})


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


@csrf_exempt
def vote_comment(request):
    if request.method == "POST":
        up = request.POST.get("up")
        down = request.POST.get("down")
        vote_id = request.POST.get("vote_id")

        method = request.POST.get("method")
        print(method, vote_id)
        try:
            vote, create, kind = get_vote_db(method, vote_id, request)
            print(vote, create, kind)
            json_resp = vote_func(vote, create, up, down, kind)
            return JsonResponse(json_resp)
        except Exception as e:
            print(e)
            return JsonResponse({"rating": "500"})



def vote_post():
    pass


@login_required
def profile(request):
    return render(request, 'user/auth.html')
