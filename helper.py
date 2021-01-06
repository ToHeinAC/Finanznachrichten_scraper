# Created by He at 06.01.2021

# Feature: helper functions etc. for the scraper, evaluation process and reporting

# Scenario: first scraper, then evaluation, then reporting

#---------------------------------------------------------

import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
#import goslate
#from deep_translator import MyMemoryTranslator
from deep_translator import GoogleTranslator
import matplotlib.pyplot as plt

###scraper
def get_content(url, write=False):
    n = datetime.datetime.now()
    now = n.strftime('%d.%m.%Y %H:%M:%S')
    # --- session ---
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    driver.implicitly_wait(10)

    driver.get(url)

    try:
        driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.quit()

    except:
        # time.sleep(1)#1s till page is loaded, set higher value if needed
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.quit()

    if write:
        with open('T_nvidia.txt', 'wb') as f:
            f.write(soup.prettify().encode())

        f.close()

    return now, soup


def get_nextpagecontent(pagenumbernext, url, write=False):
    n = datetime.datetime.now()
    now = n.strftime('%d.%m.%Y %H:%M:%S')
    # --- session ---
    #### Now if you are sure there is next page
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.implicitly_wait(5)
    driver.get(url)
    driver.implicitly_wait(5)
    # next_button_class = 'fnxui href cursor_pointer' ###here insert the class of 'next button'
    try:
        #driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/button[2]').click()
        #driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]').click()
        dummy = driver.find_element_by_class_name('seitenzahlen')
        dummy.find_elements_by_xpath('(.//span[@class = "fnxui href cursor_pointer"])')[pagenumbernext].click()
        # result= driver.find_element_by_class_name('fnxui href cursor_pointer')
        # find_elements_by_xpath('(.//span[@class = "fnxui href cursor_pointer"])')[-1].click()
        # time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.quit()

    except:
        dummy = driver.find_element_by_class_name('seitenzahlen')
        dummy.find_elements_by_xpath('(.//span[@class = "fnxui href cursor_pointer"])')[pagenumbernext].click()
        # result= driver.find_element_by_class_name('fnxui href cursor_pointer')
        # find_elements_by_xpath('(.//span[@class = "fnxui href cursor_pointer"])')[-1].click()
        # time.sleep(1)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.quit()

    return now, soup


def get_number(string):
    try:
        return int(string.replace('.', ''))
    except:
        return "Werbung"


def get_datetime(list_of_tuples):
    dummy = []
    for tupl in list_of_tuples:
        if eval(str(tupl))[1] == None:
            dummy.append(str(datetime.datetime.today().strftime('%d.%m.')) + ' | ' + str(tupl[0]))
        else:
            days = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So']
            if eval(str(tupl))[0] in days:
                dummy.append(eval(str(tupl))[1])
            else:
                dummy.append(str(tupl[0]) + ' | ' + str(tupl[1]))

    return dummy


def str_to_datetime(list_of_strings):
    '''
    formats:    '10.12. | 13:36'
                '10.12.20 | 12:00'
    '''
    dummy = []
    for string in list_of_strings:
        try:
            datetime_object = datetime.datetime.strptime(string, '%d.%m. | %H:%M')
            dummy.append(datetime_object.replace(year=datetime.datetime.now().year))
        except:
            datetime_object = datetime.datetime.strptime(string, '%d.%m.%y | %H:%M')
            dummy.append(datetime_object)

    return dummy


def get_title(soup):
    dummy = [i.span.get('title') for i in soup.find_all('td', class_='zl ft-vsbl')]
    if dummy != None:
        return dummy
    else:
        return


def get_news(soup):
    zeit = [(i.span.text, i.span.get('title')) for i in soup.find_all('td', class_='zentriert ft-vsbl ft-first-column')]
    schlagzeile = [i.span.get('title') for i in soup.find_all('td', class_='zl ft-vsbl')]
    # schlagzeile_a = [i.a.get('title') for i in soup.find_all('td', class_ = 'zl ft-vsbl')] #some are not in span class but in a class
    link = [i.a.get('href') for i in soup.find_all('td', class_="links ft-vsbl")]
    anzahl = [get_number(i.text) for i in soup.find_all('td', class_='zentriert ft-vsbl')]
    return pd.concat([pd.Series(str_to_datetime(get_datetime(zeit)), name='Zeit'),
                      pd.Series(schlagzeile, name='Schlagzeile'),
                      pd.Series(link, name='Link'),
                      pd.Series(anzahl, name='Leser')], axis=1)

###data processing and evaluations
def googletranslate_en(list_of_strings):
    return GoogleTranslator('auto', 'en').translate_batch(list_of_strings)

def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))

def plot_vaderscores(dataframe, path_to_save):
    # Group by date and ticker columns from scored_news and calculate the mean
    mean_scores = dataframe.groupby(['Aktie', 'Datum']).mean()

    # Unstack the column ticker
    mean_scores = mean_scores.unstack()

    # Get the cross-section of compound in the 'columns' axis
    mean_scores = mean_scores.xs('compound', axis="columns").transpose()

    # Plot a bar chart with pandas
    plt.figure
    mean_scores.plot(kind='bar', figsize=(12, 6), rot=30)
    plt.grid()
    plt.xlabel("Date")
    plt.ylabel("Vader Scores")
    plt.legend()
    plt.tight_layout()

    # Save the plot
    plt.savefig(path_to_save)
    plt.close()

def plot_countofnewsperday(dataframe, path_to_save):
    #Group by date and ticker columns from scored_news and calculate the count for each day
    count = dataframe.groupby(['Aktie','Datum'])['Datum'].count()
    cnt_df=pd.DataFrame(data=count)
    cnt_df=cnt_df.rename(columns={"Datum": "Anzahl"})
    cnt_df=cnt_df.reset_index(level='Datum')
    cnt_df=cnt_df.set_index('Datum')
    plt.figure
    cnt_df.plot(kind = 'bar', figsize=(12,6), rot=30)
    plt.grid()
    plt.xlabel("Date")
    plt.ylabel("Number of Occurrence")
    plt.legend()
    plt.tight_layout()
    # Save the plot
    plt.savefig(path_to_save)
    plt.close()

    return cnt_df

def plot_closeprice(dataframe, path_to_save):
    plt.figure(100)
    dataframe['Close'].plot(figsize=(12, 6), rot=30)
    plt.grid()
    plt.xlabel("Date")
    plt.ylabel("Close price in $")
    plt.legend()
    plt.tight_layout()
    # Save the plot
    plt.savefig(path_to_save)
    plt.close()
