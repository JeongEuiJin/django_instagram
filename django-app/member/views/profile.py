from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..forms import UserEditForm

User = get_user_model()
__all__ = (
    'profile',
    'profile_edit',
)

def profile(request, user_pk=None):
    if not request.user.is_authenticated and not user_pk:
        login_url = reverse('member:login')
        redirect_url = login_url + '?next='+ request.get_full_path()
        return redirect(redirect_url)

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
