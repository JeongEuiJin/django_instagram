from member.forms import LoginForm


def forms(request):
    context = {
        'login_form':LoginForm(),
    }
    return context