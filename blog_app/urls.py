from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', views.blog_home, name="home"),
    path('about/', views.blog_about, name="about"),

    # login and logout view will handle authentication, we just specify the templates to use for the views
    path('login/', LoginView.as_view(template_name='blog_app/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='blog_app/logout.html'), name="logout"),

    path('register/', views.blog_register, name="register"),

    path('new/', views.blog_new, name="new"),
    path('account/', views.blog_account, name="account"),
    path('post/<int:id>', views.blog_post, name="view_post"),

    path('delete/<int:id>', views.delete_post, name='delete'),
    path('update/<int:id>', views.update_post, name='update'),

    path('posts/<int:id>', views.posts_by, name='posts_by_user'),

    path('password-reset/', PasswordResetView.as_view(
        template_name='blog_app/reset.html'), name='password_reset'),

    path('password-reset/done', PasswordResetDoneView.as_view(
        template_name='blog_app/reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='blog_app/reset_confirm.html'), name='password_reset_confirm'),

    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='blog_app/reset_complete.html'), name='password_reset_complete'),

]
