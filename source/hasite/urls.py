from django.contrib.auth import views
from django.urls import path
from hasite.views import index, register, addpost, post, vote_comment, profile, account, index_hot, search, \
    best_choice, sendMail

app_name = "hasker"

urlpatterns = [
                path("", index, name="index"),
                path("hot/", index_hot, name="index_hot"),
                path("search/", search, name="search"),
                path("registration/", register, name="register"),
                path('auth/', views.LoginView.as_view(template_name='user/auth.html'), name='auth'),
                path('logout/', views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
                path('profile/<str:name>', profile, name="profile"),
                path('account/reset_pass/', views.PasswordChangeView.as_view(template_name='user/reset_pass.html',
                                                                             success_url = 'hasker:account'),
                                                                             name='change_password'),
                path('account/', account, name="account"),
                path('addpost/', addpost, name='addpost'),
                path('post/<int:pk>', post, name="post"),
                path('vote', vote_comment, name="vote"),
                path('best/', best_choice, name='best_choice'),
                path('email/', sendMail, name='email')

              ]
