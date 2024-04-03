from django.http import HttpRequest
from django.shortcuts import render
from django import views
from vectorSearch.VectorSearcher import vector_searcher


class MainSearchPage(views.View):
    def get(self, request: HttpRequest):
        query = request.GET.get("q", None)
        files = []
        if query:
            files = vector_searcher.search(query)
        return render(
            request,
            "index.html",
            context={
                "files": files,
                "query": query if query else "",
            },
        )