from django.contrib.auth import login as django_login, logout as django_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from member.forms import UserEditForm
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

    posts = user.post_set.order_by('-created_date')[:page * NUM_POSTS_PER_PAGE]
    post_count = user.post_set.count()
    next_page = page + 1 if post_count > page * NUM_POSTS_PER_PAGE else None

    context = {
        'cur_user': user,
        'posts': posts,
        'post_count': post_count,
        'page': page,
        'next_page': next_page,
    }
    return render(request, 'member/profile.html', context)


@require_POST
@login_required
def follow_toggle(request, user_pk):
    target_user = get_object_or_404(User, pk=user_pk)
    request.user.follow_toggle(target_user)
    if next:
        return redirect(next)
    return redirect('member:profile', user_pk=user_pk)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('member:my_profile')
    else:
        form = UserEditForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'member/profile_edit.html', context)
