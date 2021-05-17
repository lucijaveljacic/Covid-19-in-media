import matplotlib.pyplot as plt
import pandas as pd
from nltk.corpus import stopwords
from wordcloud import WordCloud


#Extracting text column to a separate .csv file
col_list = ['Tekst']
analysis = pd.read_csv("korona_podaci.csv", usecols=col_list)
analysis.to_csv('analysis.csv', index=False, header=None, encoding='utf-8-sig')

analysis_clean = open('analysis.csv', encoding='utf-8-sig').read()
analysis_clean = analysis_clean.lower()
analysis_clean = analysis_clean.replace('\t', ' ')
analysis_clean = analysis_clean.replace('\n', ' ')
#print(analysis_clean)

with open("all_words.txt", "w", encoding='utf-8-sig') as text_file:
    text_file.write(analysis_clean)




# Excluding STOPWORDS
stop = set(stopwords.words('stopwords.txt')) # Get nltk stopword list into a set.
sw_found=0 # stopwords found counter.

file = open('all_words.txt', encoding='utf-8-sig') # Open and read in a text file.
line = file.read()
words = line.split()

# If each word checked is not in stopwords list,
# then append word to a new text file.
for check_word in words:
    if not check_word.lower() in stop:
        # Not found on stopword list, so append.
        appendFile = open('words.txt', 'a', encoding='utf-8-sig')
        appendFile.write(" " +check_word)
        appendFile.close()
    else:
        # It's on the stopword list
        sw_found +=1


file = open('words.txt', 'r', encoding='utf-8-sig')
words_clean = file.read()
#print(words_clean)

#list without stopwords
words_list = words_clean.split(' ')
x = pd.value_counts(words_list).sort_index()
x = x.reset_index()
x.columns = ['Rijec', 'Count']
x = x.sort_values(by=['Count'], ascending=False).reset_index()
x = x.drop('index', 1)
print(x)
#print(x.iloc[:25])



col_list = ['Datum','Tekst']
po_danu_c = pd.read_csv('korona_podaci.csv', usecols=col_list)


po_danu_c['Text'] = po_danu_c['Tekst']
po_danu_c = po_danu_c.drop('Tekst', 1)

po_danu_c['Datum'] = pd.to_datetime(po_danu_c['Datum'])
po_danu_c = po_danu_c.value_counts().sort_index()
po_danu_c = po_danu_c.reset_index() #da se index koristi kao stupac
po_danu_c = po_danu_c.drop(po_danu_c.columns[2], axis=1)



po_mjesecu1 = po_danu_c
po_mjesecu1.Datum = pd.to_datetime(po_mjesecu1.Datum)
po_mjesecu = po_mjesecu1.groupby(pd.Grouper(key='Datum', freq='1M')).sum() # groupby each 1 month
po_mjesecu.index = po_mjesecu.index.strftime('%B')
po_mjesecu = po_mjesecu.reset_index()
po_mjesecu.columns = ['Mjesec', 'Text']
print(po_mjesecu)
po_mjesecu.to_csv('Text_po_mjesecima.csv', index=False, encoding='utf-8-sig')


February = po_mjesecu.iloc[0,1].lower().split(' ')
March = po_mjesecu.iloc[1,1].lower().split(' ')
April = po_mjesecu.iloc[2,1].lower().split(' ')
May = po_mjesecu.iloc[3,1].lower().split(' ')
June = po_mjesecu.iloc[4,1].lower().split(' ')
July = po_mjesecu.iloc[5,1].lower().split(' ')
August = po_mjesecu.iloc[6,1].lower().split(' ')
September = po_mjesecu.iloc[7,1].lower().split(' ')
October = po_mjesecu.iloc[8,1].lower().split(' ')
November = po_mjesecu.iloc[9,1].lower().split(' ')

def monthly_words(Monthly,f):
    for check_word in Monthly:
        if (not check_word.lower() in stop) and (not check_word.isspace()):
            appendFile = open(f, 'a', encoding='utf-8-sig')
            appendFile.write(" " +check_word)
            appendFile.close()


    file = open(f, 'r', encoding='utf-8-sig')
    Monthly = file.read()
    file.close()
    Monthly = Monthly.split(' ')
    filter_object = filter(lambda x: x != '', Monthly)
    Monthly = list(filter_object)

    Mon = pd.value_counts(Monthly).sort_index()
    Mon = Mon.reset_index()
    Mon.columns = ['Rijec', 'Count']
    Mon = Mon.sort_values(by=['Count'], ascending=False).reset_index()
    Mon = Mon.drop('index', 1)

    file = open(f, 'r', encoding='utf-8-sig')
    df_wordcloud = file.read()
    file.close()
    wordcloud = WordCloud(width=800, height=800,
                          max_words=25, background_color="white", collocations=False).generate(df_wordcloud)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    #plt.show()
    wordcloud.to_file(str(f)+'.png')

    return (print(Mon.iloc[:25]))


print('February:\n')
monthly_words(February, 'February.txt')
print('March:\n')
monthly_words(March, 'March.txt')
print('April:\n')
monthly_words(April, 'April.txt')
print('May:\n')
monthly_words(May, 'May.txt')
print('June:\n')
monthly_words(June, 'June.txt')
print('July:\n')
monthly_words(July, 'July.txt')
print('August:\n')
monthly_words(August, 'August.txt')
print('September:\n')
monthly_words(September, 'September.txt')
print('October:\n')
monthly_words(October, 'October.txt')
print('November:\n')
monthly_words(November, 'November.txt')

