from django.shortcuts import render
import markdown
import random

from . import util

def convert(title):
    markdowner = markdown.Markdown()
    entry = util.get_entry(title)

    if not entry:
        return None
    else:
        return markdowner.convert(entry)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html = convert(title)
    if not html:
        return render(request, "encyclopedia/error.html", {
            "message" : "The requested page was not found !"
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title" : title,
            "content" : html
        })
    
def search(request):
    query = request.POST['q']
    html = convert(query)
    if not html:
        entries = util.list_entries()
        results = []
        for entry in entries:
            if query.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/search.html", {
            "results" : results
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title" : query,
            "content" : html
        })
    
def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        entryExist = util.get_entry(title)
        if entryExist is not None:
            return render(request, "encyclopedia/error.html", {
                "message" : "The entry with this title already exists !"
            })
        else:
            html = convert(title)
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html
            })


def edit(request):
    title = request.POST['entry_title']
    content = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title" : title,
        "content" : content
    })

def save(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        
        markdowner = markdown.Markdown()
        html = markdowner.convert(content)
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html
        })
    
def rand(request):
    if request.method == "GET":
        entries = util.list_entries()
        randomEntry = random.choice(entries)
        html = convert(randomEntry)
        return render(request, "encyclopedia/entry.html", {
            "title": randomEntry,
            "content": html
        })