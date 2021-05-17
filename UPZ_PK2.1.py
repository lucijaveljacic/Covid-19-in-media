import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

lista_linkova = []

data = open('url_list.txt', encoding='utf-8-sig').read()
lista_linkova = data.split('\n')

url_count = (len(lista_linkova))
print('Total number of articles between 1.1.2020. and 30.11.2020.: ', url_count)




#Finding Covid-related articles
words = ['korona', 'koronavirus', 'koronavirusa', 'COVID', 'Covid', 'cjepivo', 'cjepiva', 'epidemija', 'epidemiolozi', 'epidemiolog', 'pandemija', 'Beroš', 'Capak', 'Markotić', 'samoizolacija', 'karantena', 'lockdown']
covid_url = []
keywords = '|'.join(words)

#Read the csv data into a dataframe
df = pd.read_csv("podaci.csv")

#Filter the data, keep the rows containing one of the keywords and write them to a csv
df = df[df["Naslov"].str.contains(keywords) | df["Tekst"].str.contains(keywords)]
df.to_csv("korona_podaci.csv", sep=",", index=False, encoding='utf-8-sig')

#df2 = pd.read_csv('korona_podaci.csv', encoding='utf-8-sig')
#Writing URL's to Covid related articles to a .txt
covid_url = df.Poveznica.to_list()
covid_count =(len(covid_url))
print('Total number of Covid-related articles: ', covid_count)

with open('url_covid.txt', 'w') as f:
    for item in covid_url:
        f.write("%s\n" % item)



# All articles - DAILY
df_all = pd.read_csv("podaci.csv")
daily_urls = df_all['Datum']
daily_urls = pd.to_datetime(daily_urls)
daily_urls = daily_urls.dt.date.value_counts().sort_index()#323 zapisa

# Covid-related articles - DAILY
df_covid = pd.read_csv('korona_podaci.csv')
daily_covid = df_covid['Datum']
daily_covid = pd.to_datetime(daily_covid)
daily_covid = daily_covid.value_counts().sort_index() #255 zapisa

daily = pd.concat([daily_urls, daily_covid], axis=1)
daily = daily.reset_index().fillna(0) #use index as column
daily.columns = ['Date', 'Total_articles', 'Covid_articles']
daily.Covid_articles = daily.Covid_articles.astype(int)
print(' ______________________________________________\n',
      'Articles by day\n',
      '----------------------------------------------\n',
      daily)
#print(type(daily))
#daily.to_csv('Clanci_po_danima.csv', index=False, encoding='utf-8-sig')

#Full table
#headers = ['Datum', 'Broj članaka', 'Covid-19 članci']
#print(tabulate(daily, headers=headers))


# All articles - MONTHLY
monthly = daily
monthly.Date = pd.to_datetime(monthly.Date)
monthly = monthly.groupby(pd.Grouper(key='Date', freq='1M')).sum() # groupby each 1 month
monthly.index = monthly.index.strftime('%B')
monthly = monthly.reset_index()
monthly.columns = ['Mjesec', 'Broj članaka', 'Covid-19 članci']
monthly['% Covid-19 članaka'] = (monthly['Covid-19 članci']/monthly['Broj članaka']).map('{:,.2%}'.format)
#print(monthly)
#monthly.to_csv('Clanci_po_mjesecima.csv', index=False, encoding='utf-8-sig')

#Full table
headers = ['Month', 'Total articles', 'Covid-19 articles', '% Covid-19 articles']
print('_______________________________________________________________________\n',
      'Articles by month\n',
      '---------------------------------------------------------------------\n',
      tabulate(monthly, headers=headers, showindex=False))



# All articles - BY CATEGORY
category_all = df_all['Kategorija']
category_all = category_all.value_counts().sort_index()
#print(category_all)

category_covid = df_covid['Kategorija']
category_covid = category_covid.value_counts().sort_index()
#print(category_covid)

by_category = pd.concat([category_all, category_covid], axis=1)
by_category = by_category.reset_index()
by_category.columns = ['Kategorija', 'Broj članaka', 'Covid-19 članci']
by_category['% Covid-19 članaka'] = (by_category['Covid-19 članci']/by_category['Broj članaka']).map('{:,.2%}'.format)

#print(by_category)
#by_category.to_csv('Clanci_po_kategorijama.csv', index=False, encoding='utf-8-sig')

#Table
headers = ['Category', 'Total articles', 'Covid-19 articles', '% Covid-19 articles']
print('_______________________________________________________________________________\n',
      'Articles by category\n',
      '----------------------------------------------------------------------------\n',
      tabulate(by_category, headers=headers, showindex=False))




# VISUALISATIONS
# a) Whole period
kon_br_link_bez_covid = url_count - covid_count
# Pie chart
labels = ['Covid articles', 'Other articles']
sizes = [covid_count, kon_br_link_bez_covid]
explode = (0.1, 0) #only explode 1st slice
colors = ['#c2c2f0', '#ffb3e6']
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.set_title('Share of Covid-19 articles between January and November 2020.')
ax1.axis('equal') #da pie bude krug
plt.tight_layout()
plt.show()


# b) By month
# Number of articles
labels = monthly['Mjesec']
covid_cl_mj = monthly['Covid-19 članci']
ostali_cl_mj = monthly['Broj članaka']-covid_cl_mj
width = 0.75
fig, ax = plt.subplots()
a=ax.bar(labels, covid_cl_mj, width, label='Covid articles', color='#c2c2f0',)
b=ax.bar(labels, ostali_cl_mj, width, bottom=covid_cl_mj, label='Other articles', color='#ffb3e6')
ax.set_ylabel('Number of articles')
ax.set_title('Number of Covid and Other articles by month')
def broj(rec):
    for rect in rec:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                  rect.get_y() + height / 2,
                  "{:.0f}".format(height),
                  ha='center',
                  va='bottom')
broj(a)
broj(b)
ax.legend()
plt.tight_layout()
plt.show()


#Percentage of articles by month
labels = monthly['Mjesec']
covid_cl_mj = (monthly['Covid-19 članci']/monthly['Broj članaka'])*100
ostali_cl_mj = 100-covid_cl_mj
width = 0.75
fig, ax = plt.subplots()
a=ax.bar(labels, covid_cl_mj, width, label='Covid articles', color='#c2c2f0',)
b=ax.bar(labels, ostali_cl_mj, width, bottom=covid_cl_mj, label='Other articles', color='#ffb3e6')
ax.set_ylabel('% of articles')
ax.set_title('Share of Covid articles in total number of articles in 2020. (monthly)')
def postotak(rec):
    for rect in rec:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                  rect.get_y() + height / 2,
                  "{:.0f}%".format(height),
                  ha='center',
                  va='bottom')
postotak(a)
postotak(b)
ax.legend()
plt.tight_layout()
plt.show()

"""
# c) Po kategorijama
labels = by_category['Kategorija']
sizes = by_category['Broj članaka']
labels_kat = ['Covid', 'Ostalo', 'Covid', 'Ostalo', 'Covid', 'Ostalo',
              'Covid', 'Ostalo', 'Covid', 'Ostalo', 'Covid', 'Ostalo',
              'Covid', 'Ostalo', 'Covid', 'Ostalo']
sizes_kat = [5,500,117,374,77,138,16,45,29,58,498,233,15,83,59,186]
colors = ['#c2c2f0','#ffb3e6', '#c2c2f0','#ffb3e6', '#c2c2f0','#ffb3e6',
          '#c2c2f0','#ffb3e6', '#c2c2f0','#ffb3e6', '#c2c2f0','#ffb3e6',
          '#c2c2f0','#ffb3e6', '#c2c2f0','#ffb3e6']
explode_kat = (0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2)
explode = (0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1)
plt.pie(sizes, labels=labels, startangle=90, frame=True,
        explode=explode_kat, radius=3)
plt.pie(sizes_kat, labels=labels_kat, colors=colors,
        radius=2, startangle=90, explode=explode)
centre_circle = plt.Circle((0, 0), 0.5, color='black', fc='white', linewidth=0)
ax1.set_title('Odnos broja Covid-19 i ostalih članaka u pojedinoj kategoriji na portalu od siječnja do studenog 2020.')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.axis('equal')
plt.tight_layout()
plt.show()
"""

# By category
labels = by_category['Kategorija']
covid_kat = by_category['Covid-19 članci']
ostalo_kat = by_category['Broj članaka']-covid_kat
width = 0.75
fig, ax = plt.subplots()
a=ax.bar(labels, covid_kat, width, label='Covid objave', color='#c2c2f0',)
b=ax.bar(labels, ostalo_kat, width, bottom=covid_kat, label='Ostale objave', color='#ffb3e6')
ax.set_ylabel('Number of articles by category')
ax.set_title('Share of Covid articles by category')
def broj(rec):
    for rect in rec:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                  rect.get_y() + height / 2,
                  "{:.0f}".format(height),
                  ha='center',
                  va='bottom')
broj(a)
broj(b)
ax.legend()
plt.tight_layout()
plt.show()
