from django import forms
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import *


class PublicSelectMultiplePaper(forms.Form):
    def get_instances(self, user):
        self.fields['papers'] = forms.ModelMultipleChoiceField(Paper.objects.filter(user=user), required=False)
        return self


class AddPaperSheet(forms.Form):
    file = forms.FileField(widget=forms.FileInput({"class": "form-control"}))
    labels = forms.ModelMultipleChoiceField(
        Label.objects.none(),
        widget=forms.SelectMultiple({"class": "form-select"}),
        required=False
    )

    def load_choices(self, user):
        self.fields['labels'].queryset = Label.objects.filter(user=user)


class DeletePaper(PublicSelectMultiplePaper):
    pass


class AddLabelInPaper(PublicSelectMultiplePaper):
    new_labels = forms.ModelMultipleChoiceField(
        Label.objects.none(),
        widget=forms.SelectMultiple({"class": "form-control"}),
        required=False
    )

    def load_choices(self, user_):
        self.fields['new_labels'].queryset = Label.objects.filter(user=user_)


class RemoveLabelInPaper(PublicSelectMultiplePaper):
    label_to_remove = forms.ModelMultipleChoiceField(
        Label.objects.none(),
        widget=forms.SelectMultiple({"class": "form-control"}),
        required=False
    )

    def load_choices(self, user_):
        self.fields['label_to_remove'].queryset = Label.objects.filter(user=user_)


class ChangeLabelInPaper(PublicSelectMultiplePaper):
    set_labels = forms.ModelMultipleChoiceField(
        Label.objects.none(),
        widget=forms.SelectMultiple({"class": "form-control"}),
        required=False
    )

    def load_choices(self, user_):
        self.fields['set_labels'].queryset = Label.objects.filter(user=user_)


class PublicSelectMultipleLabel(forms.Form):
    def get_instances(self, user_):
        self.fields['labels'] = forms.ModelMultipleChoiceField(Label.objects.filter(user=user_), required=False)
        return self


class AddLabelSheet(forms.Form):
    name = forms.CharField(widget=forms.TextInput({"class": "form-control"}))


class DeleteLabel(PublicSelectMultipleLabel):
    pass


class RenameLabel(forms.Form):
    new_name = forms.CharField(max_length=64, widget=forms.TextInput({"class": "form-control"}))


@permission_required("library.view_paper", login_url="/main?message=No permission to view papers.")
def view_library(req):
    # storage
    my_storage, created = UserStorage.objects.get_or_create(user=req.user)
    if created:
        my_storage.save()
    total_storage = my_storage.total_storage_bytes()
    used_storage = my_storage.used_storage_bytes()
    # label in paper
    add_label_in_paper = AddLabelInPaper()
    add_label_in_paper.load_choices(req.user)
    remove_label_in_paper = RemoveLabelInPaper()
    remove_label_in_paper.load_choices(req.user)
    change_label_in_paper = ChangeLabelInPaper()
    change_label_in_paper.load_choices(req.user)
    context = {
        "TotalStorage": total_storage,
        "UsedStorage": used_storage,
        "RateStorage": 0 if total_storage == 0 else used_storage / total_storage * 100,
        "Papers": Paper.objects.filter(user=req.user),
        "AddPaperSheet": AddPaperSheet(),
        "add_label_in_paper": add_label_in_paper,
        "delete_label_in_paper": remove_label_in_paper,
        "change_label_in_paper": change_label_in_paper,
    }
    return render(req, "library/main.html", context)


@permission_required("library.add_paper", login_url="/library?message=No permission.")
@csrf_exempt
@require_POST
def add_paper(req):
    sheet = AddPaperSheet(req.POST, req.FILES)
    sheet.load_choices(req.user)
    if not sheet.is_valid():
        return redirect("/library?message=Submission is not valid.")
    my_storage = UserStorage.objects.get(user=req.user)
    new_paper = Paper(user=req.user, file=sheet.cleaned_data['file'])
    if not my_storage.upload_permission(new_paper.file):
        return redirect("/library?message=Your storage is used up.")
    new_paper.save()
    new_paper.labels.set(sheet.cleaned_data['labels'])
    return redirect("/library")


@csrf_exempt
@require_POST
@permission_required("library.delete_paper", login_url="/library?message=No permission to delete papers.")
def delete_paper(req):
    dp = DeletePaper(req.POST)
    dp.get_instances(req.user)
    if not dp.is_valid():
        return redirect(f"/library?hint_info=Submission is not valid.")
    for paper in dp.cleaned_data['papers']:
        paper.delete()
    return redirect("/library")


@csrf_exempt
@require_POST
@permission_required("library.change_paper", login_url="/library?message=No permission to change papers.")
def add_label_paper(req):
    alp = AddLabelInPaper(req.POST)
    alp.get_instances(req.user)
    alp.load_choices(req.user)
    if not alp.is_valid():
        return redirect("/library?Submission is not valid.")
    for paper in alp.cleaned_data['papers']:
        for label in alp.cleaned_data['new_labels']:
            paper.labels.add(label)
    return redirect("/library")


@csrf_exempt
@require_POST
@permission_required("library.change_paper", login_url="/library?message=No permission to change papers.")
def delete_label_paper(req):
    rlp = RemoveLabelInPaper(req.POST)
    rlp.get_instances(req.user)
    rlp.load_choices(req.user)
    if not rlp.is_valid():
        return redirect("/library?Submission is not valid.")
    for paper in rlp.cleaned_data['papers']:
        for label in rlp.cleaned_data['label_to_remove']:
            paper.labels.remove(label)
    return redirect("/library")


@csrf_exempt
@require_POST
@permission_required("library.change_paper", login_url="/library?message=No permission to change papers.")
def change_label_paper(req):
    clp = ChangeLabelInPaper(req.POST)
    clp.get_instances(req.user)
    clp.load_choices(req.user)
    if not clp.is_valid():
        return redirect("/library?Submission is not valid.")
    for paper in clp.cleaned_data['papers']:
        paper.labels.set(clp.cleaned_data['set_labels'])
    return redirect('/library')


@permission_required("library.view_label", login_url="/library?message=No permission to view labels.")
def view_label(req):
    context = {
        "labels": Label.objects.filter(user=req.user),
        "add_label": AddLabelSheet(),
        "rename_label": RenameLabel(),
    }
    return render(req, "library/label.html", context)


@csrf_exempt
@require_POST
@permission_required("library.add_label", login_url="/library/label?message=No permission to add labels.")
def add_label(req):
    als = AddLabelSheet(req.POST)
    if not als.is_valid():
        return redirect("/library/label?message=Submission is not valid.")
    new_label = Label(user=req.user, name=als.cleaned_data['name'])
    new_label.save()
    return redirect("/library/label")


@csrf_exempt
@require_POST
@permission_required("library.delete_label", login_url="/library/label")
def delete_label(req):
    dls = DeleteLabel(req.POST)
    dls.get_instances(req.user)
    if not dls.is_valid():
        return redirect("/library/label?message=Submission is not valid.")
    for label in dls.cleaned_data['labels']:
        label.delete()
    return redirect('/library/label')


@csrf_exempt
@require_POST
@permission_required("library.change_label", login_url="/library/label")
def rename_label(req, label_id):
    rls = RenameLabel(req.POST)
    if not rls.is_valid():
        return redirect("/library/label?message=Submission is not valid.")
    try:
        label = Label.objects.get(id=label_id, user=req.user)
    except Label.DoesNotExist:
        return redirect("/library/label?message=This label does not exist.")
    label.name = rls.cleaned_data['new_name']
    label.save()
    return redirect('/library/label')
