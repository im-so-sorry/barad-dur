import django
from django.http import HttpResponseRedirect
from django.shortcuts import render


def return_page(request, page, context):
    return render(request, page, context)


def handler404(request):
    context = {}
    return return_page(request, "common/error_404.html", context)


def handler500(request):
    context = {}
    return return_page(request, "common/error_500.html", context)
