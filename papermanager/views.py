from random import randint

from django import forms
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import *

"""
    1. Manage Labels
"""


class PublicSelectMultipleLabel(forms.Form):
    def get_instances(self, user_):
        self.fields['label'] = forms.ModelMultipleChoiceField(Label.objects.filter(user=user_), required=False)
        return self


class NewLabel(forms.Form):
    name = forms.CharField(widget=forms.TextInput({"class": "form-control"}))


@csrf_exempt
@require_POST
@permission_required("papermanager.add_label", login_url="/library/label")
def add_label(req):
    nls = NewLabel(req.POST)
    if not nls.is_valid():
        return redirect(f"/traceback?hint_info=Submission is not valid. {nls.errors}"
                        "&retrieve=/library/label")
    new_label = Label(user=req.user, name=nls.cleaned_data['name'])
    new_label.save()
    return redirect("/library/label")


class DeleteLabel(PublicSelectMultipleLabel):
    pass


@csrf_exempt
@require_POST
@permission_required("papermanager.delete_label", login_url="/library/label")
def delete_label(req):
    dls = DeleteLabel(req.POST)
    dls.get_instances(req.user)
    if not dls.is_valid():
        return redirect(f"/traceback?hint_info=Submission is not valid. {dls.errors}"
                        "&retrieve=/library/label")
    for label in dls.cleaned_data['label']:
        label.delete()
    return redirect('/library/label')


class RenameLabel(PublicSelectMultipleLabel):
    new_name = forms.CharField(max_length=64, widget=forms.TextInput({"class": "form-control"}))


@csrf_exempt
@require_POST
@permission_required("papermanager.change_label", login_url="/library/label")
def rename_label(req):
    rls = RenameLabel(req.POST)
    rls.get_instances(req.user)
    if not rls.is_valid():
        return redirect(f"/traceback?hint_info=Submission is not valid. {rls.errors}"
                        "&retrieve=/library/label")
    if len(rls.cleaned_data['label']) != 1:
        return redirect('/traceback?hint_info=To rename a label, you should select equal to 1 of them.'
                        '&retrieve=/library/label')
    label = rls.cleaned_data['label'][0]
    label.name = rls.cleaned_data['new_name']
    label.save()
    return redirect("/library/label")


@permission_required("papermanager.view_label", login_url="/library")
def view_label(req):
    context = {
        "RenameLabel": RenameLabel(),
        "LabelTable": Label.objects.filter(user=req.user),
        "NewLabel": NewLabel({'name': f'Label-{randint(10000, 99999)}'}),
    }
    return render(req, "library/label.html", context)


"""
    2. Manage Papers
"""


class PublicSelectMultiplePaper(forms.Form):
    def get_instances(self, user):
        self.fields['papers'] = forms.ModelMultipleChoiceField(Paper.objects.filter(user=user), required=False)
        return self


class AddPaper(forms.Form):
    file = forms.FileField(widget=forms.FileInput({"class": "form-control"}))
    labels = forms.ModelMultipleChoiceField(
        Label.objects.none(),
        widget=forms.SelectMultiple({"class": "form-select"}),
        required=False
    )

    def load_choices(self, user):
        self.fields['labels'].queryset = Label.objects.filter(user=user)


@permission_required("papermanager.add_paper", login_url="/library")
@require_POST
@csrf_exempt
def add_paper(req):
    aps = AddPaper(req.POST, req.FILES)
    aps.load_choices(req.user)
    if not aps.is_valid():
        return redirect(f"/traceback?hint_info={aps.errors}&retrieve=/library")
    my_storage = UserStorage.objects.get(user=req.user)
    new_paper = Paper(user=req.user, file=aps.cleaned_data['file'])
    if not my_storage.upload_permission(new_paper.file):
        return redirect("/traceback?hint_info=Your storage has used up.&retrieve=/library")
    new_paper.save()
    new_paper.labels.set(aps.cleaned_data['labels'])
    return redirect("/library")


class DeletePaper(PublicSelectMultiplePaper):
    pass


@csrf_exempt
@require_POST
@permission_required("papermanager.delete_paper", login_url="/library")
def delete_paper(req):
    dp = DeletePaper(req.POST)
    dp.get_instances(req.user)
    if not dp.is_valid():
        return redirect(f"/traceback?hint_info={dp.errors}&retrieve=/library")
    for paper in dp.cleaned_data['papers']:
        paper.delete()
    return redirect("/library")


@permission_required("papermanager.view_paper", login_url="/home")
def view_paper(req):
    # storage
    my_storage, created = UserStorage.objects.get_or_create(user=req.user)
    if created:
        my_storage.save()
    total_storage = my_storage.total_storage_bytes()
    used_storage = my_storage.used_storage_bytes()
    # paper manager
    ap = AddPaper()
    ap.load_choices(req.user)
    cl = ChangeLabel()
    cl.load_choices(req.user)

    context = {
        "TotalStorage": total_storage,
        "UsedStorage": used_storage,
        "RateStorage": 0 if total_storage == 0 else used_storage / total_storage * 100,
        "Papers": Paper.objects.filter(user=req.user),
        "AddPaper": ap, "ChangeLabel": cl,
    }
    return render(req, "library/main.html", context)


"""
    3. Advanced Functions
    3.1. Paper -> Label
"""


class ChangeLabel(PublicSelectMultiplePaper):
    mode = forms.ChoiceField(
        choices=[('A', "Add"), ('R', "Remove"), ('S', "Set As")],
        widget=forms.Select({"class": "form-select"}),
    )
    labels = forms.ModelMultipleChoiceField(
        Label.objects.none(),
        widget=forms.SelectMultiple({"class": "form-select"}),
        required=False
    )

    def load_choices(self, user):
        self.fields['labels'].queryset = Label.objects.filter(user=user)


@permission_required("papermanager.change_paper", login_url="/library")
@csrf_exempt
@require_POST
def change_paper_s_label(req):
    cl = ChangeLabel(req.POST)
    cl.load_choices(req.user)
    cl.get_instances(req.user)
    if not cl.is_valid():
        return redirect(f"/traceback?hint_info={cl.errors}&retrieve=/library")

    if cl.cleaned_data['mode'] == 'A':
        for label in cl.cleaned_data['labels']:
            for paper in cl.cleaned_data['papers']:
                paper.labels.add(label)
    elif cl.cleaned_data['mode'] == 'R':
        for label in cl.cleaned_data['labels']:
            for paper in cl.cleaned_data['papers']:
                paper.labels.remove(label)
    elif cl.cleaned_data['mode'] == 'S':
        for paper in cl.cleaned_data['papers']:
            paper.labels.set(cl.cleaned_data['labels'])
    return redirect("/library")
