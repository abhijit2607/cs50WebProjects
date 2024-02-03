from random import choice

from django.shortcuts import render

from django import forms

from . import util

from markdown2 import markdown


def convert_md_to_html(title):
    content = util.get_entry(title)
    if content is None:
        return None
    else:
        return markdown(content)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "title": "Encyclopedia",
        "heading": "All Pages"
    })


def entry(request, name):
    content = convert_md_to_html(name)
    if content is None:
        return render(request, "encyclopedia/entry.html", {
            "title": "404",
            "html": "<h1> ERROR!!! PAGE DOES NOT EXIST </h1>"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": name.upper(),
            "html": content
        })


def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        content = convert_md_to_html(entry_search)
        if content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search.upper(),
                "html": content,
            })
        else:
            all_entries = util.list_entries()
            recommandation = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recommandation.append(entry)

            if not recommandation:  # Empty list is considered false in boolean context in python
                return render(request, "encyclopedia/entry.html", {
                    "title": "404",
                    "html": "<h1> ERROR!!! PAGE DOES NOT EXIST </h1>"
                })
            else:
                return render(request, "encyclopedia/index.html", {
                    "entries":recommandation,
                    "title": "Suggestions",
                    "heading": "Search Result Recommandations"
                })
