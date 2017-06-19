from django.shortcuts import redirect


def main_post(request):
    return redirect('post:post_list')