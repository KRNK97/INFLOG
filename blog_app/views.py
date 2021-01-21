from django.shortcuts import render, redirect
from .models import Post, Profile, User
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, UserUpdateForm, ProfileUpdateForm, PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def blog_home(request):

    all_posts = Post.objects.all().order_by('-id')

    if len(all_posts) == 0:
        context = {
            "title": "Blog Home"
        }
        return render(request, "blog_app/home.html", context)

    paginator = Paginator(all_posts, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)

    # if page is not number i.e maybe a character
    except PageNotAnInteger:
        posts = paginator.page(1)

    # if page num doesnt exist then take to last page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "title": "Blog Home",
        "posts": posts
    }

    return render(request, "blog_app/home.html", context)


def blog_about(request):
    context = {
        "title": "Blog About"
    }

    return render(request, "blog_app/about.html", context)


def blog_register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # cleaned data is avai only after validation
            name = form.cleaned_data.get('username')
            form.save()
            messages.success(
                request, f'Account succesfully created for {name}. Now you can login')
            form = RegistrationForm()
            return redirect('login')
    else:
        form = RegistrationForm()

    context = {
        "title": "Blog Register",
        "form": form
    }

    return render(request, "blog_app/register.html", context)


@login_required
def blog_new(request):

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        # since there is no author itself, we need to add it or we will get null error
        form.instance.author = request.user
        form.save()
        messages.success(
            request, f'Succesfully posted')
        return redirect('home')

    context = {
        "title": "New Post",
        "form": form
    }

    return render(request, "blog_app/new.html", context)


@login_required
def update_post(request, id):
    post = Post.objects.filter(id=id).first()
    form = PostForm(instance=post)

    if request.method == 'POST':
        post.author = request.user
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        messages.success(
            request, f'Post succesfully updated')
        return redirect('view_post', id=post.id)

    context = {
        "title": "Update Post",
        "form": form,
    }

    return render(request, "blog_app/update.html", context)


@login_required
def blog_account(request):
    # user = User.objects.filter(username=name).first()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # we need to save file data as well from profile
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(
                request, f'Account succesfully updated')
            return redirect('account')

    else:
        # as user forms and profile form are model forms, we can directly pass in thier instances to populate the fields already
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        "title": "User Account",
        "u_form": u_form,
        "p_form": p_form
    }

    return render(request, "blog_app/account.html", context)


@login_required
def blog_post(request, id):
    post = Post.objects.filter(id=id).first()

    context = {
        "title": post.title,
        "post": post
    }

    return render(request, "blog_app/post.html", context)


@login_required
def delete_post(request, id):
    post = Post.objects.filter(id=id).first()

    if request.method == 'POST':
        post.delete()
        print('post deleted')
        messages.success(
            request, f'Post deleted')

        return redirect('home')

    context = {
        "title": post.title,
        "author": post.author
    }

    return render(request, "blog_app/delete.html", context)


@login_required
def posts_by(request, id):
    all_posts = Post.objects.filter(author_id=id).order_by('-id')
    author = User.objects.filter(id=id).first()
    # print(username)
    paginator = Paginator(all_posts, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        "author": author.username,
        "posts": posts
    }

    return render(request, "blog_app/posts_by.html", context)
