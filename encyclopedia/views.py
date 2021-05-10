from django.shortcuts import render

from . import util
import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
import random


class NewEntry(forms.Form):
    title = forms.CharField(label='Entry Title', widget=forms.TextInput(
        attrs={'class': 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(label='Markdown Content', widget=forms.Textarea(
        attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))


class EditEntry(forms.Form):
    content = forms.CharField(label='Markdown Content', widget=forms.Textarea(
        attrs={'class': 'form-control col-md-8 col-lg-8', 'rows': 10}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def article(request, article):
    markdowner = markdown.Markdown()
    articlePage = util.get_entry(article)
    if articlePage is None:
        return render(request, "encyclopedia/noarticle.html", {
            "articleTitle": article
        })
    else:
        return render(request, "encyclopedia/article.html", {
            "article": markdowner.convert(articlePage),
            "articleTitle": article
        })


def search(request):
    value = request.GET.get("q")
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("article", kwargs={"article": value}))
    else:
        substringSearch = []
        for articleTitle in util.list_entries():
            if value.upper() in articleTitle.upper():
                substringSearch.append(articleTitle)

        return render(request, "encyclopedia/search.html", {
            "entries": substringSearch,
            "search": True,
            "value": value
        })


def newEntry(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if(util.get_entry(title) is None):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("article", kwargs={"article": title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                    "form": form,
                    "existing": True,
                    "article": title
                })
    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": NewEntry(),
            "existing": False,
        })


def editEntry(request, article):

    if request.method == 'POST':
        markdowner = markdown.Markdown()
        articlePage = util.get_entry(article)
        form = EditEntry(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(article, content)
        return HttpResponseRedirect(reverse("article", kwargs={"article": article}))
    else:
        articlePage = util.get_entry(article)
        initial_data = {
            "content": articlePage
        }
        form = EditEntry(initial=initial_data)
        return render(request, "encyclopedia/editEntry.html", {
            "form": form,
            "article": article,
            "articlePage": articlePage
        })


def randomArticle(request):
    articles = util.list_entries()
    articleTitle = random.choice(articles)
    article = util.get_entry(articleTitle)
    return HttpResponseRedirect(reverse("article", kwargs={"article": articleTitle}))
