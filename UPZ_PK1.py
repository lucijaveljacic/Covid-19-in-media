import requests
import bs4
from csv import writer
from datetime import datetime
import re
import json
import pandas as pd


konacna_lista_linkova = []

data = open('url_list.txt', encoding='utf-8').read()
konacna_lista_linkova = data.split('\n')
linkovi = konacna_lista_linkova

with open('podaci.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
    csv_writer = writer(csv_file)
    headers = ['ID', 'Poveznica', 'Naslov', 'Kategorija', 'Datum', 'Dan', 'Vrijeme', 'Tekst', 'Glasovi']
    csv_writer.writerow(headers)

with open('podaci.json', 'w') as json_file:
    headers = ['ID', 'Poveznica', 'Naslov', 'Kategorija', 'Datum', 'Dan', 'Vrijeme', 'Tekst', 'Glasovi']
    json.dump(headers, json_file)

category = {
    "gospodarstvo": "Economy",
    "politika": "Politics",
    "samouprava": "Self-government",
    "crna-kronika": "Crime&Accidents",
    "kultura": "Culture",
    "drutvo": "Society",
    "sport": "Sport",
    "zanimljivosti": "Interesting facts"
}

month = {
    "Siječanj": "01",
    "Veljača": "02",
    "Ožujak": "03",
    "Travanj": "04",
    "Svibanj": "05",
    "Lipanj": "06",
    "Srpanj": "07",
    "Kolovoz": "08",
    "Rujan": "09",
    "Listopad": "10",
    "Studeni": "11"
}



for i in range(0,2433):
    print('URL: ', i+1)
    row = []

    res = requests.get(linkovi[i])
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    link_split = linkovi[i].split('/')
    #print(link_split)


    #ID
    link_split_ID = link_split[5].split('-')
    ID = link_split_ID[0]
    #print(ID)
    row.append(ID)


    #Poveznica (URL)
    poveznica = linkovi[i]
    #print(poveznica)
    row.append(poveznica)


    #Naslov (Title)
    title = soup.find('h2', class_='itemTitle')
    for j in title:
        naslov = j
    naslov1 = naslov.split('\t')
    naslov2 = naslov1[5].split('\n')
    naslov = naslov2[0]
    #print(naslov)
    row.append(naslov)


    #Kategorija (Category)
    kategorija = category[link_split[3]]
    #print(kategorija)
    row.append(kategorija)


    #DATUM, DAN, VRIJEME
    date_time = soup.find('span', class_='itemDateCreated')
    for j in date_time:
        dt = j
    dt1 = dt.split('\t')
    dt = dt1[3]

    #Datum (Date)
    datum1 = dt.split(' ')
    datum1[2] = month[datum1[2]]
    datum1 = datum1[1:4]
    s1 = ' '
    datum1 = s1.join(datum1)
    datum = datetime.strptime(datum1, '%d %m %Y').date()
    #print(datum)
    row.append(datum)

    #Dan (Day)
    day = dt.split(',')
    dan = day[0]
    #print(dan)
    row.append(dan)

    #Vrijeme (Time)
    vrijeme1 = dt.split(' ')
    vrijeme1 = vrijeme1[4]
    vrijeme = datetime.strptime(vrijeme1, '%H:%M').time()
    #print(vrijeme)
    row.append(vrijeme)


    #Tekst (Text)
    blok1 = soup.find('div', class_='itemFullText')
    blok = blok1.find_all('p')
    tekst1 = str(blok)

    tekst1 = re.sub('<[^>]*>', '', tekst1)
    tekst1 = re.sub('//[^>]*//-->', '', tekst1)

    tekst = tekst1
    tekst = tekst.replace('\n', '')
    tekst = tekst.replace('\t', '')
    tekst = re.sub(r'\W+', ' ', tekst)

    #print (tekst)
    row.append(tekst)

    #Glasovi (Votes)
    votes = soup.find('div', class_='itemRatingLog')
    for j in votes:
        vote = j
    glasovi = vote.split(' ')
    glasovi = glasovi[0].split('(')
    glasovi = glasovi[1]
    #print(glasovi)
    row.append(glasovi)

    with open('podaci.csv', 'a', newline='', encoding='utf-8-sig') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(row)


csv_file = pd.DataFrame(pd.read_csv("podaci.csv", sep = ",", header = 0, index_col = False))
csv_file.to_json("podaci.json", orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)
