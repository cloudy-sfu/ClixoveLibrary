from django import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Register

"""
    1. Track Errors
"""


class TracebackForm(forms.Form):
    hint_info = forms.CharField()
    retrieve = forms.CharField()


def track_errors(req):
    tf = TracebackForm(req.GET)
    if tf.is_valid():
        context = {
            "hint_info": tf.cleaned_data['hint_info'],
            "retrieve": tf.cleaned_data['retrieve'],
        }
    else:
        context = {
            "hint_info": f"Unknown errors: {tf.errors}",
            "retrieve": "home",
        }
    return render(req, "mylogin/traceback.html", context)


"""
    2. Log in and Log out
"""


class LoginSheet(forms.Form):
    username = forms.CharField(max_length=64, required=True,
                               widget=forms.TextInput({"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput({"class": "form-control"}),
                               max_length=64, required=True)


def login_view(req):
    context = {
        "LoginSheet": LoginSheet(),
    }
    return render(req, "mylogin/home.html", context)


@require_POST
@csrf_exempt
def my_login(req):
    sheet1 = LoginSheet(req.POST)
    if not sheet1.is_valid():
        return redirect("/traceback?hint_info=Login form is not valid."
                        "&retrieve=/home")
    user = authenticate(req,
                        username=sheet1.cleaned_data['username'],
                        password=sheet1.cleaned_data['password'])
    if not user:
        return redirect("/traceback?hint_info=Username or password is not correct."
                        "&retrieve=/home")
    login(req, user)
    return redirect('/library')


@login_required(login_url='/home')
def my_logout(req):
    logout(req)
    return redirect('/home')


"""
    3. Register
"""


class RegisterSheet(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput({"class": "form-control"}),
        label="Username", min_length=4, max_length=16,
        help_text="<small class=text-muted>English characters and digits (6-18) only.</small>",
    )
    password = forms.CharField(
        widget=forms.PasswordInput({"class": "form-control"}),
        label="Password",
        min_length=4, max_length=16,
        help_text="<small class=text-muted>English characters and digits (4-16) only.</small>",
    )
    password_again = forms.CharField(
        widget=forms.PasswordInput({"class": "form-control"}),
        label="Password Again",
        min_length=4, max_length=16,
    )
    bio = forms.CharField(
        widget=forms.Textarea({"class": "form-control"}),
        label="Biography", required=False, max_length=500,
        help_text="<small class=text-muted>Information that is showed to admission staffs of the group. "
                  "Max lengthen 500 characters.</small>"
    )
    group = forms.ModelMultipleChoiceField(
        Group.objects.all(),
        widget=forms.SelectMultiple({"class": "form-control"}),
        help_text="<small class=text-muted>Hold down “Control”, or “Command” on a Mac, to select more "
                  "than one.</small>"
    )


def register_view(req):
    context = {
        'RegisterSheet': RegisterSheet(),
    }
    return render(req, "mylogin/register.html", context)


@csrf_exempt
@require_POST
def register(req):
    register_sheet = RegisterSheet(req.POST)
    if not (
            register_sheet.is_valid() and
            register_sheet.cleaned_data['password'] == register_sheet.cleaned_data['password_again']
    ):
        return redirect("/traceback?hint_info=Two fields of password are not the same, or the form is not valid."
                        f"{register_sheet.errors}"
                        "&retrieve=/mylogin/register")
    new_register = Register(
        username=register_sheet.cleaned_data['username'],
        password=register_sheet.cleaned_data['password'],
        bio=register_sheet.cleaned_data['bio'],
    )
    new_register.save()
    new_register.group.set(register_sheet.cleaned_data['group'])
    return redirect('/mylogin/register')


"""
    4. Admit and reject
"""


class PublicApplicationSelection(forms.Form):
    def get_instances(self, groups):
        self.fields['application'] = forms.ModelMultipleChoiceField(
            Register.objects.filter(group__in=groups), required=False,
        )
        return self


class AdmitSheet(PublicApplicationSelection):
    action = forms.ChoiceField(
        choices=[('A', 'Admit'), ('R', 'Reject')],
        widget=forms.Select({"class": "form-select", "aria-label": "Default select example"}),
    )
    group = forms.ModelChoiceField(
        Group.objects.none(),
        widget=forms.Select({"class": "form-select", "aria-label": "Default select example"}),
        label="To which group?"
    )

    def load_choices(self, groups):
        self.fields['group'].queryset = groups


@permission_required('mylogin.view_register', login_url='/library')
def admission_view(req):
    groups = req.user.groups.all()
    ams = AdmitSheet()
    ams.load_choices(groups)
    context = {
        'NewUserTable': Register.objects.filter(group__in=groups).distinct(),
        'AdmitSheet': ams,
    }
    return render(req, "mylogin/admission.html", context)


@permission_required(['mylogin.delete_register', 'auth.add_user'], login_url='/library')
@csrf_exempt
@require_POST
def admit(req):
    groups = req.user.groups.all()
    ams = AdmitSheet(req.POST)
    ams.get_instances(groups)
    ams.load_choices(groups)
    if not ams.is_valid():
        return redirect(f"/traceback?hint_info=The submission is not valid. {ams.errors}"
                        "&retrieve=/mylogin/admission/")
    represented_group = ams.cleaned_data['group']
    if ams.cleaned_data['action'] == 'R':
        for application in ams.cleaned_data['application']:
            application.group.remove(represented_group)
            if application.group.count() == 0:
                application.delete()
    elif ams.cleaned_data['action'] == 'A':
        for application in ams.cleaned_data['application']:
            new_user, created = User.objects.get_or_create(username=application.username)
            if created:
                new_user.set_password(application.password)
                new_user.save()
            elif not authenticate(username=application.username, password=application.password):
                continue
            new_user.groups.add(represented_group)
            application.group.remove(represented_group)
            if application.group.count() == 0:
                application.delete()
    return redirect('/mylogin/admission/')
