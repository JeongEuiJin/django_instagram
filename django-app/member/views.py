from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from .forms import LoginForm
from .forms import SigupForm

User = get_user_model()


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post:post_list')


    else:
        if request.user.is_authenticated:
            return redirect('post:post_list')
        form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == 'POST':
        form = SigupForm(data=request.POST)
        if form.is_valid():
            user = form.create_user()
            django_login()
            return redirect('post:post_list')
    else:
        form = SigupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)


def profile(request, user_pk=None):
    NUM_POSTS_PER_PAGE = 3
    page = request.GET.get('page', 1)
    try:
        page = int(page) if int(page) > 1 else 1

    except ValueError:
        page = 1

    except Exception as e:
        page = 1
        print(e)

    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
    else:
        user = request.user

    posts = user.post_set.filter(author=user).order_by('-created_date')[:NUM_POSTS_PER_PAGE * 9]
    post_count = user.post_set.filter(author=user).count()
    next_page = page + 1 if post_count > NUM_POSTS_PER_PAGE * 9 else None

    context = {
        'cur_user': user,
        'posts': posts,
        'post_count': post_count,
        'page': page,
        'next_page':next_page,
    }
    return render(request, 'member/profile.html', context)
