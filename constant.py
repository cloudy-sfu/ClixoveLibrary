from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


class TracebackForm(forms.Form):
    hint_info = forms.CharField()
    retrieve = forms.CharField()


@csrf_exempt
@login_required
def traceback(req):
    tf = TracebackForm(req.GET)
    if not tf.is_valid():
        return HttpResponse("Server error. Please click \"Back\" button on the browser.", status=404)
    context = {
        "hint_info": tf.cleaned_data['hint_info'],
        "retrieve": tf.cleaned_data['retrieve'],
    }
    return render(req, "traceback.html", context)


bs5_input = {"class": "form-control form-group"}
