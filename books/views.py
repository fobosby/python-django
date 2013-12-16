from django.shortcuts import render_to_response
from books.models import Book


def search_form(request):
    return render_to_response('search/SearchTemplate.html')


def search_results(request):
    if 'search_string' in request.GET:
        var = Book.objects.filter(title__icontains=request.GET['search_string'])
        return render_to_response('search/SearchResults.html', {'result': var, 'sys_info': request.META})
    else:
        return render_to_response('search/SearchResults.html',{'sys_info': request.META})