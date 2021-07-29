from django.shortcuts import render
from .models import PatternTable
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

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
            p = PatternTable(name = name, link = link, description = new_des_text, category = group)
            p.save()


def index(request):
    #webScrape()
    #return(HttpResponse("hello"))
    return render(request, "patterns/index.html", {"patterns": PatternTable.objects.all()})

#def pattern(request, pid):
