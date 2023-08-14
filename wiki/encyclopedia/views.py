from django.shortcuts import render

from . import util

from markdown2 import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, name):
    try:
        return render(request, "encyclopedia/entry.html", {
            "title": name.upper(),
            "html": markdown(util.get_entry(name))
        })
    except TypeError:
        return render(request, "encyclopedia/entry.html", {
            "title": "ERROR",
            "html": "<h1>ERROR!!! PAGE DOES NOT EXIST</h1>"
        })