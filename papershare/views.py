from django import forms
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import *

"""
    1. Manage Paper -> Link
"""


class PublicSelectMultiplePaper(forms.Form):
    def get_instances(self, user):
        self.fields['papers'] = forms.ModelMultipleChoiceField(Paper.objects.filter(user=user), required=False)
        return self


class AddLink(PublicSelectMultiplePaper):
    pass


@csrf_exempt
@require_POST
@permission_required('papershare.add_link', login_url='/library')
def add_link(req):
    al = AddLink(req.POST)
    al.get_instances(req.user)
    if not al.is_valid():
        return redirect(f"/traceback?hint_info={al.errors}&retrieve=/library")
    new_link = Link(from_user=req.user)
    new_link.save()
    new_link.papers.set(al.cleaned_data['papers'])
    return redirect(f'/share/link/id={new_link.id}')


@permission_required('papershare.view_link', login_url='/library')
def view_link(req, id_):
    this_link = Link.objects.get(id=id_)
    context = {
        "ViewLink": this_link,
    }
    return render(req, "share/link_page.html", context)


"""
    2. Manage Link List
"""


@permission_required('papershare.view_link', login_url='/library')
def view_link_list(req):
    context = {
        "LinkTable1": Link.objects.filter(from_user=req.user),
        "LinkTable2": Link.objects.filter(to_user__in=[req.user]),
    }
    return render(req, "share/main.html", context)
