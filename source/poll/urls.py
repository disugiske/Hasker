from django.urls import path
from poll.views import (
    index,
    addpost,
    post,
    vote_comment,
    profile,
    index_hot,
    search,
    best_choice,
)

app_name = "poll"

urlpatterns = [
    path("", index, name="index"),
    path("hot/", index_hot, name="index_hot"),
    path("search/", search, name="search"),
    path("search/tag/<str:tag>", search, name="searchtag"),
    path("search/word/<str:word>", search, name="searchword"),
    path("profile/<str:name>", profile, name="profile"),
    path("addpost/", addpost, name="addpost"),
    path("post/<int:pk>", post, name="post"),
    path("vote", vote_comment, name="vote"),
    path("best/", best_choice, name="best_choice"),
]
