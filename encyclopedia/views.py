from django.shortcuts import render
from markdown import markdown
from django import forms
from django.http import HttpResponseRedirect

from . import util

class SearchForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search encyclopedia', 'class':'search'}))

class NewPageForm(forms.Form):
    
    title = forms.CharField(label="Title", widget=(forms.TextInput(attrs={'placeholder':'Title'})))
    content = forms.CharField(label="Text", widget=(forms.Textarea(attrs={'placeholder':'Content'})))

    def clean_title(self):
        title = self.cleaned_data["title"]
        title = str(title)
        if util.compare(title):
            raise forms.ValidationError("This entity is already exist")
        return title

class EditPageForm(forms.Form):
    
    def __init__(self, title="", content="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['readonly'] = True
        self.fields['title'].initial = title
        self.fields['content'].initial = content

    title = forms.CharField(label="Title")
    content = forms.CharField(label="Text", widget=(forms.Textarea()))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "form":SearchForm(), "entries": util.list_entries(),
    })

def title(request, title):
    return render(request, "encyclopedia/title.html",{
        "form":SearchForm(), "text": markdown(util.get_entry(title)), "title": title
        })

def search(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        title = str(title)
        for i in util.list_entries():
            if title == i:
                return HttpResponseRedirect(f"wiki/{title}")
    else:
        return render(request, "encyclopedia/search.html",{
        "form":form
    })
    return render(request, "encyclopedia/search.html",{
        "form":SearchForm(), "title": util.searching(title)
    })

def random(rquest):
    randomTitle = util.random()
    return HttpResponseRedirect(f"wiki/{randomTitle}")

def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title,content)
            return HttpResponseRedirect(f"wiki/{title}")
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form":SearchForm, "newPageForm":form
            })

    return render(request, "encyclopedia/new_page.html", {
        "form":SearchForm() ,"newPageForm":NewPageForm()
    })

def editPage(request, title):
    if request.method == "POST":
        form = EditPageForm(data = request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            editedContent = form.cleaned_data["content"]
            util.save_entry(title, editedContent)
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "form":SearchForm(), "editPageForm":form, "title":title
            })
    return render(request, "encyclopedia/edit_page.html", {
        "form":SearchForm(), "editPageForm":EditPageForm(title, util.get_entry(title)), "title":title
    })