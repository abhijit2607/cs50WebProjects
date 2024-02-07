from random import choice

from django import forms

from django.shortcuts import render

from django import forms

from . import util

from markdown2 import markdown


class NewEntry(forms.Form):
    new_entry_title = forms.CharField(label="TITLE", widget=forms.TextInput(
        attrs={"style": "width:250px", "placeholder": "Enter the title..."}))
    new_entry_content = forms.CharField(label="", widget=forms.Textarea(
        attrs={"style": "width:1000px; height:400px;", "placeholder": "Enter the Markdown Content... "}))
    new_entry_save_button = forms.CharField(
        label="", widget=forms.TextInput(attrs={"type": "submit", "value": "Save"}))


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
                    "entries": recommandation,
                    "title": "Suggestions",
                    "heading": "Search Result Recommandations"
                })


def new_page(request):
    entries = util.list_entries()

    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["new_entry_title"]
            content = form.cleaned_data["new_entry_content"]

            if title in entries:
                return render(request, "encyclopedia/entry.html", {
                    "title": "Error",
                    "html": "<h1> ERROR!!! PAGE ALREADY EXISTS"
                })
            else:
                util.save_entry(title, content)
                content = convert_md_to_html(title)
                return render(request, "encyclopedia/entry.html", {
                    "title": title.upper(),
                    "html": content
                })

        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": NewEntry()
        })


def random(request):
    entries = util.list_entries()
    random_page_title = choice(entries)
    content = convert_md_to_html(random_page_title)
    return render(request, "encyclopedia/entry.html", {
        "title": random_page_title.upper(),
        "html": content
    })
