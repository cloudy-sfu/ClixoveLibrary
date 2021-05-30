from django import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import *


class LoginSheet(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput({"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput({"class": "form-control"}),
                               max_length=150, min_length=4)


def view_login(req):
    context = {"LoginSheet": LoginSheet()}
    return render(req, "my_login/login.html", context)


@require_POST
@csrf_exempt
def add_login(req):
    sheet1 = LoginSheet(req.POST)
    if not sheet1.is_valid():
        return redirect('/main?message=Login form is not valid.')
    user = authenticate(req,
                        username=sheet1.cleaned_data['username'],
                        password=sheet1.cleaned_data['password'])
    if not user:
        return redirect('/main?message=Username or password is not correct.')
    login(req, user)
    return redirect('/library')


@login_required(login_url='/main')
def delete_login(req):
    logout(req)
    return redirect('/main')


class RegisterSheet(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput({"class": "form-control"}),
        label="Username", max_length=150,
        help_text="<small class=text-muted>English characters and digits (1-150) only.</small>",
    )
    password = forms.CharField(
        widget=forms.PasswordInput({"class": "form-control"}),
        label="Password",
        min_length=4, max_length=150,
        help_text="<small class=text-muted>English characters and digits (4-150) only.</small>",
    )
    password_again = forms.CharField(
        widget=forms.PasswordInput({"class": "form-control"}),
        label="Password Again",
        min_length=4, max_length=150,
    )
    bio = forms.CharField(
        widget=forms.Textarea({"class": "form-control"}),
        label="Biography", required=False,
        help_text="<small class=text-muted>Information that is showed to admission staffs of the group. "
                  "Max lengthen 500 characters.</small>"
    )
    group = forms.ModelChoiceField(
        Group.objects, initial=Group.objects.first(),
        widget=forms.Select({"class": "form-select"}),
        help_text="<small class=text-muted>Hold down “Control”, or “Command” on a Mac, to select more "
                  "than one.</small>",
    )


def view_register(req):
    context = {
        'RegisterSheet': RegisterSheet(),
    }
    return render(req, "my_login/register.html", context)


@csrf_exempt
@require_POST
def add_register(req):
    register_sheet = RegisterSheet(req.POST)
    if not register_sheet.is_valid():
        return redirect("/my_login/register?message=Submission is not valid.")
    if not register_sheet.cleaned_data['password'] == register_sheet.cleaned_data['password_again']:
        return redirect("/my_login/register?message=The twice password don't match.")
    new_register = Register(
        username=register_sheet.cleaned_data['username'],
        password=register_sheet.cleaned_data['password'],
        bio=register_sheet.cleaned_data['bio'],
        group=register_sheet.cleaned_data['group']
    )
    new_register.save()
    return redirect("/my_login/register?message=Success.&success=1")
