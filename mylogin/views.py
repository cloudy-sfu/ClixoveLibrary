from django import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ClixoveLibrary.constant import bs5_input
from .models import Register


class LoginSheet(forms.Form):
    username = forms.CharField(max_length=64, required=True,
                               widget=forms.TextInput(bs5_input))
    password = forms.CharField(widget=forms.PasswordInput(bs5_input),
                               max_length=64, required=True)


def login_view(req):
    context = {
        "LoginSheet": LoginSheet(),
    }
    return render(req, "mylogin/home.html", context)


@require_POST
@csrf_exempt
def mylogin(req):
    sheet1 = LoginSheet(req.POST)
    if not sheet1.is_valid():
        return redirect('/traceback/login-form-not-valid/home')
    user = authenticate(req,
                        username=sheet1.cleaned_data['username'],
                        password=sheet1.cleaned_data['password'])
    if not user:
        return redirect('/traceback/password-error/home')
    login(req, user)
    return redirect('/library')


class RegisterSheet(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(bs5_input),
        label="Username", min_length=6, max_length=18,
        required=True,
        help_text="<small class=text-muted>English characters and digits (6-18) only.</small>",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(bs5_input),
        label="Password", required=True,
        min_length=4, max_length=16,
        help_text="<small class=text-muted>English characters and digits (4-16) only.</small>",
    )
    password_again = forms.CharField(
        widget=forms.PasswordInput(bs5_input),
        label="Password Again", required=False,
        min_length=4, max_length=16,
    )
    bio = forms.CharField(
        widget=forms.Textarea(bs5_input),
        label="Biography", required=False, max_length=500,
        help_text="<small class=text-muted>Information that is showed to admission staffs of the group. "
                  "Max lengthen 500 characters.</small>"
    )
    group = forms.ModelMultipleChoiceField(
        Group.objects.all(),
        widget=forms.SelectMultiple(bs5_input),
        required=True,
        help_text="<small class=text-muted>Press `Ctrl` to select multiple values.<br>Press `Shift` to select "
                  "continuous values.</small>"
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
        return redirect('/traceback/register-form-not-valid/register')
    new_register = Register(
        username=register_sheet.cleaned_data['username'],
        password=register_sheet.cleaned_data['password'],
        bio=register_sheet.cleaned_data['bio'],
    )
    new_register.save()
    new_register.group.set(register_sheet.cleaned_data['group'])
    return redirect('/mylogin/register')


@login_required(login_url='/home')
def mylogout(req):
    logout(req)
    return redirect('/home')


@permission_required('mylogin.view_register', login_url='/library')
def waitlist_view(req):
    context = {
        'NewUserTable': Register.objects.filter(group__in=req.user.groups.all()),
    }
    return render(req, "mylogin/admission.html", context)


class ReceivedApplication(forms.Form):
    action = forms.ChoiceField(choices=('Admit', 'Reject'))

    def load_choices(self, user):
        groups = user.groups.all()
        self.fields['application'] = forms.ModelMultipleChoiceField(Register.objects.filter(group__in=groups))


@permission_required('mylogin.delete_register', login_url='/library')
@csrf_exempt
@require_POST
def admit(req):
    ra = ReceivedApplication(req.POST)
    if not ra.is_valid():
        return redirect("/traceback/sheet-not-valid/admission")
    if ra.cleaned_data['action'] == 'Reject':
        for application in ra.cleaned_data['application']:
            application.delete()
    elif ra.cleaned_data['action'] == 'Admit':
        for application in ra.cleaned_data['application']:
            new_user, created = User.objects.get_or_create(username=application.username)
            if created:
                new_user.set_password(application.password)
                new_user.save()
                new_user.groups.set(application.group)
            else:
                user = authenticate(username=application.username, password=application.password)
                if user:
                    user.groups.set(user.groups.all() | application.group)
            application.delete()
    return redirect('/library')
