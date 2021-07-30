from django.shortcuts import render
from .models import PatternTable, Category
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django import forms
class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))
# Create your views here.

def webScrape():
    import bs4
    from urllib.request import urlopen as uReq
    from bs4 import BeautifulSoup as soup
    import sqlite3
    my_url = 'https://www.amigurumi.com/search/free/'
  
    for page in range (1,11): #parse 10 pages
        new_url = my_url + str(page) + '/'
        uClient = uReq(new_url)
        page_html = uClient.read()
        uClient.close()
        page_soup=soup(page_html, "html.parser")
        containers = page_soup.findAll("div", {"class":"item"})
        
        for i in range(len(containers)): #Go through each item
            container = containers[i]
            # Name of pattern
            name = container.img.get('title')
            # Link to pattern
            link = container.a.get('href')

            #Parse each link to pattern
            newClient = uReq(link)
            new_html = newClient.read()
            newClient.close()
            pattern_soup = soup(new_html, "html.parser")

            # Description of pattern
            description = pattern_soup.findAll("div", {"id": "patterndescription"})
            
            if len(description)!=0:
                des = description[0]
                des_text = des.find('p').text.strip()
                new_des_text="".join(des_text.splitlines())
            else: 
                new_des_text = " "
            # What category pattern belongs in
            category = pattern_soup.findAll("span", {"itemprop": "title"})
            
            group = category[1].text
            obj, created = Category.objects.get_or_create(cate=group)
            p = PatternTable(name = name, link = link, description = new_des_text, category = obj)
            p.save()


def index(request):
    #webScrape()
    #return(HttpResponse("hello"))
    if request.GET.get('q'):
        query = request.GET.get("q", "")
        return(search(request, query))
    else:
        return render(request, "patterns/index.html", {"patterns": PatternTable.objects.all()})


def pattern(request, pattern_id):
    pattern = PatternTable.objects.get(id=pattern_id)
    return render(request, "patterns/pattern.html", {"pattern":pattern})

def search(request, query):
    patterns = PatternTable.objects.all()
    results=[]
    for pattern in patterns:
        if query.lower() == pattern.name.lower():
            return render(request, "patterns/pattern.html",{"pattern": pattern})
        if query.lower() in pattern.name.lower() or query.lower() in pattern.description.lower():
            results.append(pattern)

    return render(request,"patterns/search.html", {"results":results})   

def categories(request):
    results = Category.objects.all()
    return render(request, "patterns/categories.html",{"results": results})

def category(request,cate_id):
    #patterns_match = PatternTable.objects.filter(category=cate)
    c = Category.objects.get(id = cate_id)
    all_patterns = c.patterns_incategory.all()
    return render(request, "patterns/category.html", {"all_patterns": all_patterns, "c":c})