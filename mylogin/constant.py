from django.shortcuts import render


def short_link(token):
    links_contain_folder = {
        'register': 'mylogin/register',
        'admission': 'mylogin/waitlist/',
        'projects': 'library/projects',
    }
    if token in links_contain_folder.keys():
        return links_contain_folder[token]
    else:
        return token


def traceback(request, guidance, retrieve):
    context = {"hint_info": content[guidance], "retrieve": short_link(retrieve)}
    return render(request, "traceback.html", context)


content = {
    'login-form-not-valid': 'Login form is not valid.',
    'password-error': 'Username or password is not correct.',
    'register-form-not-valid': 'Two fields of password are not the same, or the form is not valid.',
    'sheet-not-valid': 'The submission is not valid.',
    'file-exceed': 'You storage has used up, and there isn\'t enough space for this file.',
}
bs5_input = {"class": "form-control form-group"}
