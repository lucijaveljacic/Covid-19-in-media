import requests
import bs4

konacna_lista_linkova = []

def get_links(poveznica, z, poveznica2):
    svi_linkovi = []
    print('Page: ', 1)

    res = requests.get(poveznica)
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    linkovi = []
    date = soup.find_all('span', {'class': 'catItemDateCreated'})
    blok1 = soup.find('div', class_='itemList')
    blok = blok1.find_all('h3', class_='catItemTitle')

    datumi = []

    for j in date:
        datum = j
        new_j = []
        for rijeci in datum:
            new_j.extend(rijeci.split())
        datumi.append(new_j)

    for el in blok:
        link = el.find('a')
        linkovi.append(link['href'])

    linkovi2020 = []

    for i in range(z, 10):
        if (datumi[i][3] == '2020') & (datumi[i][2] != 'Prosinac'):
            linkovi2020.append(linkovi[i])

    svi_linkovi += linkovi2020
    print('Number of links: ', len(svi_linkovi))

    godina = 2020

    while godina >= 2020:
        for s in range(1, 1000):
            print('Page: ', s + 1)
            res = requests.get(poveznica2 + str(s) + '0')
            soup = bs4.BeautifulSoup(res.text, 'lxml')

            linkovi = []
            date = soup.find_all('span', {'class': 'catItemDateCreated'})
            blok1 = soup.find('div', class_='itemList')
            blok = blok1.find_all('h3', class_='catItemTitle')

            datumi = []

            for j in date:
                datum = j
                new_j = []
                for rijeci in datum:
                    new_j.extend(rijeci.split())
                datumi.append(new_j)

            for el in blok:
                link = el.find('a')
                linkovi.append(link['href'])

            linkovi2020 = []

            for i in range(0, 10):
                if (datumi[i][3] == '2020') & (datumi[i][2] != 'Prosinac'):
                    linkovi2020.append(linkovi[i])
                else:
                    if (datumi[i][3] == '2019'):
                        godina = 2019
                        break

            svi_linkovi += linkovi2020
            print('Number of links: ', len(svi_linkovi))

            if godina == 2019:
                break

    return svi_linkovi



def category_link_list(x):
    y = len(x) #number of links
    print(y)

    for i in range(0, y):
        x[i] = 'https://pozeska-kronika.hr' + x[i]

    lista_linkova = []
    lista_linkova += x
    return lista_linkova


#GOSPODARSTVO
svi_linkovi_gosp = get_links('https://pozeska-kronika.hr/gospodarstvo.html', 1, 'https://pozeska-kronika.hr/gospodarstvo.html?start=')
konacna_lista_linkova += category_link_list(svi_linkovi_gosp)

#POLITIKA
svi_linkovi_pol = get_links('https://pozeska-kronika.hr/politika.html', 0, 'https://pozeska-kronika.hr/politika.html?start=')
konacna_lista_linkova += category_link_list(svi_linkovi_pol)

#SAMOUPRAVA
svi_linkovi_sam = get_links('https://pozeska-kronika.hr/samouprava.html', 0, 'https://pozeska-kronika.hr/samouprava.html?start=')
konacna_lista_linkova += category_link_list(svi_linkovi_sam)

#CRNA KRONIKA
svi_linkovi_ck = get_links('https://pozeska-kronika.hr/crna-kronika.html', 0, 'https://pozeska-kronika.hr/crna-kronika.html?start=')
konacna_lista_linkova += category_link_list(svi_linkovi_ck)

#KULTURA
svi_linkovi_kul = get_links('https://pozeska-kronika.hr/kultura.html', 0, 'https://pozeska-kronika.hr/kultura.html?start=')
konacna_lista_linkova += category_link_list(svi_linkovi_kul)

#DRUSTVO
svi_linkovi_dru = get_links('https://pozeska-kronika.hr/drutvo.html', 0, 'https://pozeska-kronika.hr/drutvo.html?start=')
konacna_lista_linkova += category_link_list(svi_linkovi_dru)

#SPORT
svi_linkovi_sp = get_links('https://pozeska-kronika.hr/sport.html', 0, 'https://pozeska-kronika.hr/sport.html?start=')
konacna_lista_linkova += category_link_list(svi_linkovi_sp)

#ZANIMLJIVOSTI
svi_linkovi_zan = get_links('https://pozeska-kronika.hr/zanimljivosti.html', 0, 'https://pozeska-kronika.hr/zanimljivosti.html?start=')
konacna_lista_linkova += category_link_list(svi_linkovi_zan)


kbroj_linkova=len(konacna_lista_linkova)


with open('url_list.txt', 'w', encoding='utf-8-sig') as f:
    for item in konacna_lista_linkova:
        f.write("%s\n" % item)

print(f"Number of web pages between January and November 2020: {kbroj_linkova}")
