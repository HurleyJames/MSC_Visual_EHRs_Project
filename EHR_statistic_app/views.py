# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    """
    跳转链接
    :param request:
    :return:
    """
    return HttpResponseRedirect("/datagrid")


def datagrid(request):
    return HttpResponse("Data Grid")
