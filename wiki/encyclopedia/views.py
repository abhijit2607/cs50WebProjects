from random import choice

from django import forms

from django.shortcuts import render

from django import forms

from . import util

from markdown2 import markdown


class Entry(forms.Form):
    entry_title = forms.CharField(label="TITLE", widget=forms.TextInput(
        attrs={"style": "width:250px", "placeholder": "Enter the title..."}))
    entry_content = forms.CharField(label="", widget=forms.Textarea(
        attrs={"style": "width:1000px; height:400px;", "placeholder": "Enter the Markdown Content... "}))
    entry_save_button = forms.CharField(
        label="", widget=forms.TextInput(attrs={"type": "submit", "value": "Save"}))


class EditButton(forms.Form):
    edit_button = forms.CharField(label="", widget=forms.TextInput(
        attrs={"type": "submit", "value": "Edit"}), required=False)



def convert_to_lower(list):
    return [element.lower() for element in list]


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
        return render(request, "encyclopedia/error.html", {
            "title": "404",
            "html": "<h1> ERROR!!! PAGE DOES NOT EXIST </h1>"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": name.upper(),
            "html": content,
            "form": EditButton()
        })


def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        content = convert_md_to_html(entry_search)
        if content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search.upper(),
                "html": content,
                "form": EditButton()
            })
        else:
            all_entries = util.list_entries()
            recommandation = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recommandation.append(entry)

            if not recommandation:  # Empty list is considered false in boolean context in python
                return render(request, "encyclopedia/error.html", {
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
    entries = convert_to_lower(util.list_entries())

    if request.method == "POST":
        form = Entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entry_title"]
            content = form.cleaned_data["entry_content"]

            if title.lower() in entries:
                return render(request, "encyclopedia/error.html", {
                    "title": "ALREADY EXISTS",
                    "html": "<h1> ERROR!!! PAGE ALREADY EXISTS"
                })
            else:
                util.save_entry(title, content)
                content = convert_md_to_html(title)
                return render(request, "encyclopedia/entry.html", {
                    "title": title.upper(),
                    "html": content,
                    "form": EditButton()
                })

        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "form": Entry()
        })


def edit_page(request):
    if request.method == "POST":
        title = request.POST["entry_title"]
        content = util.get_entry(title)
        
        form = Entry(initial={
            "entry_title": title,
            "entry_content": content
        })
        return render(request, "encyclopedia/edit.html", {
            "form": form
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "title": "FORBIDDEN",
            "html": "<h1>Error!!! Can only be accessed using Edit button in the entry pages..."
        })
    

def save_entry(request):
    if request.method == "POST":
        form = Entry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["entry_title"]
            content = form.cleaned_data["entry_content"]

        util.save_entry(title, content)

        content = convert_md_to_html(title)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "html": content,
            "form": EditButton()
        })
    
    else:
        return render(request, "encyclopedia/error.html", {
            "title": "FORBIDDEN",
            "html": "<h1>Error!!! Can only be accessed using Save button in the edit pages..."
        })


def random(request):
    entries = util.list_entries()
    random_page_title = choice(entries)
    content = convert_md_to_html(random_page_title)
    return render(request, "encyclopedia/entry.html", {
        "title": random_page_title.upper(),
        "html": content,
        "form": EditButton()
    })
