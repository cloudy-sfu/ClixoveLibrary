from random import randint

from django import forms
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from ClixoveLibrary.constant import bs5_input
from papershare.models import ShareLink
from papershare.views import ShareBox
from .models import *
"""
    Function 1: New Paper
"""


class AddPaperSheet(forms.Form):
    file = forms.FileField(widget=forms.FileInput(bs5_input))

    def load_project_menu(self, user):
        self.fields['project'] = forms.ModelMultipleChoiceField(
            widget=forms.SelectMultiple(bs5_input),
            queryset=Project.objects.filter(user=user),
            label="Labels",
        )


@permission_required('papermanager.add_paper', login_url='/library')
@require_POST
@csrf_exempt
def add_paper(req):
    add_paper_sheet = AddPaperSheet(req.POST, req.FILES)
    add_paper_sheet.load_project_menu(req.user)
    if not add_paper_sheet.is_valid():
        return redirect('/traceback/sheet-not-valid/add-paper')
    new_paper = Paper(
        user=req.user,
        file=add_paper_sheet.cleaned_data['file']
    )
    new_paper.save()
    new_paper.project.set(add_paper_sheet.cleaned_data['project'])
    my_storage = UserStorage.objects.get(user=req.user)
    if not my_storage.upload_permission(new_paper.file):
        return redirect('/traceback/file-exceed/library')
    new_paper.save()
    return redirect('/library')


"""
    Function 2: New Label
"""


class NewLabelSheet(forms.Form):
    name = forms.CharField(widget=forms.TextInput(bs5_input))


@permission_required('papermanager.add_project', login_url='/library')
@csrf_exempt
@require_POST
def add_label(req):
    new_project_raw = NewLabelSheet(req.POST)
    if not new_project_raw.is_valid():
        return redirect('/traceback/sheet-not-valid/library')
    new_project = Project(user=req.user, name=new_project_raw.cleaned_data['name'])
    new_project.save()
    return redirect('/library/projects')


"""
    Function 3: Change Labels
"""


class MoveTo(forms.Form):
    def load_choices(self, user):
        self.fields['project'] = forms.ModelMultipleChoiceField(
            widget=forms.SelectMultiple(bs5_input),
            label='Move To',
            queryset=Project.objects.filter(user=user),
            required=False
        )


"""
    Function 4: Delete Labels
"""


class DeleteProjectSheet(forms.Form):
    def load_choices(self, user):
        self.fields['project'] = forms.ModelMultipleChoiceField(
            Project.objects.filter(user=user)
        )


@permission_required('papermanager.delete_project', login_url='/library')
@csrf_exempt
@require_POST
def delete_label(req):
    dps = DeleteProjectSheet(req.POST)
    dps.load_choices(req.user)
    if not dps.is_valid():
        redirect('traceback/sheet-not-valid/projects')
    for project in dps.cleaned_data['project']:
        project.delete()
    return redirect('/library/projects')


"""
    Main: Paper Management
"""


class ChangePaperSheet(forms.Form):
    action = forms.CharField(widget=forms.Select(choices=['Delete', 'Move']))

    def load_choices(self, user):
        self.fields['paper'] = forms.ModelMultipleChoiceField(Paper.objects.filter(user=user))
        self.fields['project'] = forms.ModelMultipleChoiceField(Project.objects.filter(user=user), required=False)
        self.fields['users'] = forms.ModelMultipleChoiceField(
            User.objects.filter(groups__in=user.groups.all()), required=False)


@permission_required('papermanager.view_paper', login_url="/home")
@csrf_exempt
@require_POST
def change_papers(req):
    cps = ChangePaperSheet(req.POST)
    cps.load_choices(req.user)
    if not cps.is_valid():
        return redirect('/traceback/sheet-not-valid/library')
    if cps.cleaned_data['action'] == 'Delete' and \
            req.user.has_perm('papermanager.delete_paper'):
        for paper in cps.cleaned_data['paper']:
            paper.delete()
    elif cps.cleaned_data['action'] == 'Move' and \
            req.user.has_perm('papermanager.change_paper'):
        for paper in cps.cleaned_data['paper']:
            paper.project.set(cps.cleaned_data['project'])
    elif cps.cleaned_data['action'] == 'Share' and \
            req.user.has_perm('papershare.add_sharelink'):
        sl = ShareLink(user_from=req.user)
        sl.save()
        sl.users_to.set(cps.cleaned_data['users'])
        sl.papers.set(cps.cleaned_data['paper'])
    return redirect('/library')


"""
    Main: Views
"""


@permission_required('papermanager.view_project', login_url='/library')
def labels_view(req):
    context = {
        "ProjectsTable": Project.objects.filter(user=req.user),
        "NewProject": NewLabelSheet({'name': f'Label-{randint(10000, 99999)}'}),
    }
    return render(req, "library/labels.html", context)


@permission_required('papermanager.view_paper', login_url="/home")
def library_view(req):
    my_storage, created = UserStorage.objects.get_or_create(user=req.user)
    if created:
        my_storage.save()
    total_space = my_storage.total_storage_bytes()
    used_space = my_storage.used_storage_bytes()
    rate_space = 0 if total_space == 0 else used_space / total_space * 100
    add_paper_sheet = AddPaperSheet()
    add_paper_sheet.load_project_menu(req.user)
    move_to = MoveTo()
    move_to.load_choices(req.user)
    context = {
        "Papers": Paper.objects.filter(user=req.user),
        "TotalStorage": total_space, "UsedStorage": used_space, "RateStorage": rate_space,
        "NewPaper": add_paper_sheet,
        "MoveTo": move_to,
        "shared_sheet": ShareBox(),
        "shared_paper": Paper.objects.filter(sharelink__users_to__in=[req.user]),
    }
    return render(req, "library/main.html", context)
