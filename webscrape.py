import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import sqlite3

my_url = 'https://www.amigurumi.com/search/free/'
#Connect to sqlite3 database
#conn = sqlite3.connect('my_database.db')
#cur = conn.cursor()
#cur.execute('''CREATE TABLE IF NOT EXISTS my_table(pattern TEXT,link TEXT,description TEXT,category TEXT)''')
# Open csv file
#filename = "patterns.csv"
#f = open(filename, "w")
#headers = "pattern, link, description, category\n"
#f.write(headers)
for page in range (1,2): #parse 10 pages
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
        p = PatternTable(name, link, new_des_text, group)
        #f.write(name + "," +  link + "," + new_des_text.replace(",", " ") + ","  + group + "\n")
        #cur.execute('''INSERT INTO my_table(pattern,link, description, category) VALUES(?,?,?,?)''', (name, link, new_des_text, group))
        #conn.commit()
#f.close()
#cur.execute('''SELECT * FROM my_table ''')
#results= cur.fetchall()
#print(results)
#cur.close()
#conn.close()