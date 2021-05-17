# __Covid 19 in media__

This project was made as a part of a course called Knowledge Management (Upravljanje znanjem). 

<b>Faculty:</b> Department of Informatics, University of Rijeka

<b>Author:</b>
* Lucija Veljačić
  
<b>Mentor:</b>
* izv. prof. dr. sc. Ana Meštrović
  
<b>Programming language:</b> Python 3

<hr>

## Description

The purpose of this project is to analyze data collected from a Croatian web portal  [Požeška kronika](https://pozeska-kronika.hr) and to generate new knowledge based on this data.

The __first part__ of the project focuses on collecting and cleaning data from the web portal. After scraping, the data is saved to a .csv file for future use in the second part of the project.

The goal of the __second part__ of the project is to analyze the collected data in regards to the current pandemic of Covid-19.  The analysis of the articles provided an insight into the presence of Covid-19 in the media.


  
### Požeška kronika - Homepage

<div style="text-align:center" >

<img src="photos/pk.png" width="1000" style="text-align:center" >

</div>

<br>

### Technical information

__OS:__ Windows 10

__Tools and software:__
* PyCharm
* Python 3.8

__Packages:__
* requests (2.25.1)
* bs4 (0.0.1)
* regex (2021.4.4)
* pandas (1.2.4)
* tabulate (0.8.9)
* matplotlib (3.4.2)
* nltk (3.6.2)
* wordcloud (1.8.1)

<hr>

## Phase 1 - Web scraping

### Script __UPZ_PK0.py__

The script collects unique URLs from the web portal for the period from __1.1.2020. to 30.11.2020.__ and stores them in the file __url_list.txt__.

Web portal has __8 categories__:
* Economy
* Politics
* Self-government
* Crime&Accidents
* Culture
* Society
* Sport
* Interesting facts

Function __get_links__ is called for each category of the portal separately and it goes through pages containing the short overview of the articles (10 articles per page), starting from the newest page and stopping when it finds an article written before 1.1.2020. For a URL to be stored in the list of URLs, it must meet the condition that it is from 2020 and that it was not written in December, since the analysis is performed until the end of November. The final list of URLs has 2433 records. 

When executing the code, the script prints the number of pages it has opened for each category and the number of articles from the page that meet the condition of being published between 1.1.2020. and 30.11.2020. It also prints the total number of URLs after each page and the current category, and prints it. 

### Script __UPZ_PK1.py__

The next script __UPZ_PK1.py__ uses a previously created file storing URLs to get the list of URLs. The script opens each URL and scrapes the article ID, URL, title, category, date, day, and time of publishing, as well as article text and number of votes (number of people who reacted to the article).

Collected data and corresponding headers are stored in a file __podaci.csv__.  Initially, only the headers are stored, and then the data for each article is stored separately, as a row, as the script goes through the list of URLs. At the end, the data from the .csv file is read and stored to a .json file with the same name.

The format of the collected data can be seen in the following image.

<div style="text-align:center" >

<img src="photos/data.png" width="700" style="text-align:center" >

</div>

<br>

<hr>

## Phase 2 - Analysis

The goal of the Phase 2 is to to analyze the data in regards to the current pandemic of Covid-19. In other words, to see how often and when the articles mentioned the pandemic.

### Script __UPZ_PK2.1.py__

This script quantifies the number of Covid-related articles and visualizes the data.

In order to find the articles that mention Covid-19, it was necessary to create a list of keywords. Chosen words are:

* korona, koronavirus, koronavirusa, Covid, Covid, cjepivo, cjepiva, epidemija, epidemiolozi, epidemiolog, pandemija, Beroš, Capak, Markotić, samoizolacija, karantena, lockdown

The script reads the data from __podaci.csv__ into a DataFrame and after that it checks whether one of the keywords is mentioned either in the title or the text of each article. Only the records (articles) containing one of the keywords are kept in the DataFrame and stored in the file __korona_podaci.csv__. Additionally, the script creates another .txt file, __url_covid.txt__, containing only the URLs of the Covid-related articles. The script calculates the total number of articles and Covid-related articles and creates a Pie Chart showing the share of Covid-related articles in the total number articles, as shown in the images below. 

<div style="text-align:center" >

<img src="photos/count.png" width="500" style="text-align:center" >

</div>

<br>


<div style="text-align:center" >

<img src="photos/pie.png" width="500" style="text-align:center" >

</div>

<br>

It is visible from the Pie Chart that a little bit over 1/3 (35,1%) of the articles in the given period of time mentioned Covid-19.

Additional analyzes were conducted to compare the share of Covid articles during a particular day, month, or within a web portal category.

__Daily__

<div style="text-align:center" >

<img src="photos/6.png" width="500" style="text-align:center" >

</div>

<br>

__Monthly__

<div style="text-align:center" >

<img src="photos/7.png" width="500" style="text-align:center" >

</div>

<br>

<div style="text-align:center" >

<img src="photos/2.png" width="500" style="text-align:center" >

</div>

<br>

<div style="text-align:center" >

<img src="photos/3.png" width="500" style="text-align:center" >

</div>

<br>

__By Category__

<div style="text-align:center" >

<img src="photos/8.png" width="500" style="text-align:center" >

</div>

<br>

<div style="text-align:center" >

<img src="photos/4.png" width="500" style="text-align:center" >

</div>

<br>






 
