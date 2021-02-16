from django import forms
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from ClixoveLibrary.constant import bs5_input
from .models import *


class ShareBox(forms.Form):
    search = forms.CharField(
        widget=forms.TextInput({"id": "share-user-question",
                                "onkeydown": "search1(event)",
                                **bs5_input}),
        required=False,
        help_text="<small class=\"text-muted\">Press \"Enter\" to search by other's username.<br>"
                  "You can only find people in your groups.</small>",
        label="Find people",
    )
    users = forms.MultipleChoiceField(
        widget=forms.SelectMultiple({"id": "share-user-answer", **bs5_input}),
        choices=[], required=False, label="Share with",
        help_text="<small class=\"text-muted\">Press `Ctrl` to select multiple values. <br> Press `Shift` "
                  "to select continuous values.</small>"
    )

    def load_choices(self, name_search, user):
        groups = user.groups.all()
        self.filtered_users = User.objects.filter(username__contains=name_search, groups__in=groups)
        self.fields['users'].choices = [(x.id, x.username) for x in self.filtered_users]

    def load_defaults(self, selected_users):
        self.filtered_users = self.filtered_users | selected_users
        self.fields['users'].choices = [(x.id, x.username) for x in self.filtered_users]
        self.fields['users'].initial = [x.id for x in selected_users]


class ReceivedShareBox(forms.Form):
    def receive_jquery(self, user):
        groups = user.groups.all()
        self.fields['search_content'] = forms.CharField(required=True)
        self.fields['shared_user_[]'] = forms.ModelMultipleChoiceField(
            User.objects.filter(groups__in=groups), required=False
        )


@permission_required('papershare.add_sharelink')
def shared_user_search(req):
    sb = ShareBox()
    received_sb = ReceivedShareBox(req.GET)
    received_sb.receive_jquery(req.user)
    if not received_sb.is_valid():
        return HttpResponse(sb.as_p())
    sb.load_choices(received_sb.cleaned_data['search_content'], req.user)
    if 'shared_user_[]' in received_sb.cleaned_data.keys():
        sb.load_defaults(received_sb.cleaned_data['shared_user_[]'])
    return HttpResponse(sb.as_p())


@permission_required('papershare.view_sharelink', login_url='/library')
def shared_link_view(req):
    context = {
        "ProjectsTable": ShareLink.objects.filter(user_from=req.user),
    }
    return render(req, "share/links.html", context)


class DeleteProjectSheet(forms.Form):
    def load_choices(self, user):
        self.fields['project'] = forms.ModelMultipleChoiceField(
            ShareLink.objects.filter(user_from=user)
        )


@permission_required('papermanager.delete_project', login_url='/library')
@csrf_exempt
@require_POST
def delete_label(req):
    dps = DeleteProjectSheet(req.POST)
    dps.load_choices(req.user)
    if not dps.is_valid():
        redirect('traceback/sheet-not-valid/share')
    for project in dps.cleaned_data['project']:
        project.delete()
    return redirect('/share')
