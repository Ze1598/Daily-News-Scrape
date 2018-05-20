'''
Scrape news titles and its URLs from a set of websites then 
save them to a .txt file.
'''

'''
TODO:
    In each website scraping, create a string with html for
the news. This will be another thing to be returned for each
function call.
    Create a web page (HTML+CSS) to present the articles
(title and URL). For groupings of news (i.e., news from
Eurogamer, from Wccftech, ...) maybe have a logo of the
website.
    Scrape news from more websites: Jornal de Notícias,
more subreddits (Switch, PS4,Python, Learn Python, ...)
'''

# Used to make GET requests
# http://docs.python-requests.org/en/master/
from requests import get
# Used to create objects from the scraped source code
# https://beautiful-soup-4.readthedocs.io/en/latest/
from bs4 import BeautifulSoup
# Used to deal with date and time
from datetime import date, datetime
# Used to start files (specifically, the created .txt file)
from os import startfile
# Used to time how long the script takes to run
from time import time
# Used to interact with Reddit's API
# https://praw.readthedocs.io/en/latest/
import praw
# File with credentials for the Reddit API
import Ze1598Bot_credentials as cred
# Used to open URLs in the default browser
# import webbrowser

def scrape_eurogamer():
    '''Scrape Eurogamer.net today's news.'''

    return_string = 'Eurogamer.net:\n'
    target = get('http://www.eurogamer.net').text
    soup = BeautifulSoup(target, 'html5lib')
    html_temp = '''\n\n\n\t\t<div id="Eurogamer">
            <ul type="none">'''

    # A mapping of the scraped news and its URLs
    # news_mapping = {}

    articles = soup.find('div', class_='small-list').find_all('div', class_='list-item ')
    for article in articles:
        url = 'http://www.eurogamer.net' + article.p.a['href']
        # try/except clause because not all articles use the <span> tag
        # If an article does, remove that content from the article's title, else\
        # just scrape the article's title
        try:
            # The text under the <span> tag is used to identify videos, recommended\
            # articles or Digital Foundry articles
            span_text = article.p.a.span.text.strip()
            # Remove the <span> tag text
            title = article.p.a.text.strip().replace(span_text, "")
            # news_mapping[title] = url
        except:
            title = article.p.a.text.strip()
            # news_mapping[title] = url
        html_temp += f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>'

        return_string += f'-"{title}":\n\t{url}\n'

    html_temp += '''\n\t\t\t</ul>
        </div>'''

    # return (return_string, news_mapping)
    return (return_string, html_temp)


def scrape_wccftech():
    '''Scrape Wccftech's top 6 featured news.'''
    return_string = 'Wccftech:\n'
    target = get('https://wccftech.com/').text
    soup = BeautifulSoup(target, 'html5lib')
    html_temp = '''\n\n\t\t<div id="Wccftech">
            <ul type="none">'''

    # A mapping of the scraped news and its URLs
    # news_mapping = {}

    for i in range(1,7):
        article = soup.find('a', class_='featured featured-'+str(i))
        title = article.h2.text
        url = article['href']
        # news_mapping[title] = url
        return_string += f'-"{title}":\n\t{url}\n'
        html_temp += f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>'
    
    html_temp += '''\n\t\t\t</ul>
        </div>'''

    # return (return_string, news_mapping)
    return (return_string, html_temp)    


def scrape_bbc_news():
    '''Scrape the top 6 featured news from BBC World News.'''

    return_string = 'BBC World:\n'
    target = get('http://www.bbc.com/news/world').text
    soup = BeautifulSoup(target, 'html5lib')
    html_temp = '''\n\n\t\t<div id="BBC World News">
            <ul type="none">'''

    # A mapping of the scraped news and its URLs
    # news_mapping = {}

    # Article at the top
    top_article = soup.find('div', class_="buzzard-item")
    title = top_article.a.h3.text.strip()
    url = 'http://www.bbc.com' + top_article.a['href'].strip()
    # news_mapping[title] = url
    return_string += f'-"{title}":\n\t{url}\n'
    html_temp += f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>'


    # First and second columns (each contains a single news article)
    column = soup.find_all('div', class_='pigeon__column pigeon__column--a')
    for article in column:
        title = article.a.h3.text.strip()
        url = 'http://www.bbc.com' + article.a['href'].strip()
        # news_mapping[title] = url
        return_string += f'-"{title}":\n\t{url}\n'
        html_temp += f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>'
    
    # Third column (contains 3 news)
    column = soup.find('div', class_='pigeon__column pigeon__column--b').find_all('div', class_='pigeon-item faux-block-link')
    for article in column:
        title = article.a.h3.text.strip()
        url = 'http://www.bbc.com' + article.a['href'].strip()
        # news_mapping[title] = url
        return_string += f'-"{title}":\n\t{url}\n'
        html_temp += f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>'

    html_temp += '''\n\t\t\t</ul>
        </div>'''

    # return (return_string, news_mapping)
    return (return_string, html_temp)    


def scrape_science_mag():
    '''Scrape the first page of Latest News from Science Magazine.'''

    return_string = 'Science Magazine:\n'
    target = get('http://www.sciencemag.org/').text
    soup = BeautifulSoup(target, 'html5lib')
    html_temp = '''\n\n\t\t<div id="Science Magazine">
            <ul type="none">'''

    # A mapping of the scraped news and its URLs
    # news_mapping = {}

    articles = soup.find('ul', class_='tabbed__panel tabbed__grid').find_all('li')
    for post in articles:
        title = post.article.h2.a.text.strip()
        url = 'http://www.sciencemag.org' + post.article.h2.a['href']
        # news_mapping[title] = url
        return_string += f'-"{title}":\n\t{url}\n'
        html_temp += f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>'

    html_temp += '''\n\t\t\t</ul>
        </div>'''
    
    # return (return_string, news_mapping)
    return (return_string, html_temp)    


def scrape_reddit_tech():
    '''Scrape the fist 5 posts in r/ technology's Hot section 
    using Reddit's API.'''

    return_string = 'r/ Technology:\n'
    subreddit_instance = reddit_instance.subreddit('technology')
    html_temp = '''\n\n\t\t<div id="r/ Technology">
            <ul type="none">'''
    
    # A mapping of the scraped news and its URLs
    # news_mapping = {}
    
    first_5_hot = list(subreddit_instance.hot(limit=7))
    # Delete subreddit-specific posts
    del first_5_hot[0:2]
    for post in first_5_hot:
        # news_mapping[post.title] = post.url
        return_string += f'-"{post.title}":\n\t{post.url}\n'
        html_temp += f'\n\t\t\t<li><a href="{post.url}" target="_blank">{post.title}</a></li>'
    
    html_temp += '''\n\t\t\t</ul>
        </div>'''

    # return (return_string, news_mapping)
    return (return_string, html_temp)


def scrape_reddit_world_news():
    '''Scrape the fist 5 posts in r/ worldnews's Hot section
    using Reddit's API.'''

    return_string = 'r/ WorldNews:\n'
    subreddit_instance = reddit_instance.subreddit('worldnews')
    html_temp = '''\n\n\t\t<div id="r/ WorldNews">
            <ul type="none">'''

    # A mapping of the scraped news and its URLs
    # news_mapping = {}

    first_5_hot = list(subreddit_instance.hot(limit=5))
    for post in first_5_hot:
        # news_mapping[post.title] = post.url
        return_string += f'-"{post.title}":\n\t{post.url}\n'
        html_temp += f'\n\t\t\t<li><a href="{post.url}" target="_blank">{post.title}</a></li>'

    html_temp += '''\n\t\t\t</ul>
        </div>'''

    # return (return_string, news_mapping)
    return (return_string, html_temp)    


if __name__ == '__main__':
    # Time how long it takes to run the script
    start_time = time()
    # Get today's date
    today = date.today()
    # Get the current hour
    hour = datetime.now().hour
    
    # Start the string to be written to the file
    if hour < 12:
        write_string = f'{today}_{hour}AM news\n\n'
    elif hour >= 12:
        write_string = f'{today}_{hour-12}PM news\n\n'

    # Define the name of the file to be written
    if hour < 12:
        file_name = f'{today}_{hour}AM_news'
        # file_name = str(today) + '_' + str(hour) + 'AM_news.txt'
    elif hour >= 12:
        file_name = f'{today}_{hour-12}PM_news'
        # file_name = str(today) + '_' + str(hour) + 'PM_news.txt'

    '''
    # Dictionary with the mappings of the scraped news and its URLs
    news = {}
    '''

    # The string to hold the HTML to be written to the file
    html_string = f'''<!DOCTYPE html>
<html>
    <head>
        <title>Daily News Scrape</title>
        <meta charset="ISO-8859-1">
        <link rel="stylesheet" type="text/css" href="news.css">
    </head>
    
    <body>
        <div class="page-header" id="page-top">
            <h1 class="title">Daily News Scrape</h1>
            <h2 class="date">{today}</h2>
        </div>'''

    # Call each function to scrape data and save the returned\
    # results. Since the returned result for each function is a\
    # tuple where the first item is a string to be written to the\
    # file and the second is a mapping of the website's news\ 
    # titles and URLs, update the contents of that dictionary
    # to the 'news' dictionary.

    eurogamer = scrape_eurogamer()
    # news.update(eurogamer[1])

    wccftech = scrape_wccftech()
    # news.update(wccftech[1])
    
    bbc_news = scrape_bbc_news()
    # news.update(bbc_news[1])
    
    science_mag = scrape_science_mag()
    # news.update(science_mag[1])
    
    # Create a Reddit instance for API access
    reddit_instance = praw.Reddit(client_id = cred.client_id, client_secret = cred.client_secret, user_agent = cred.user_agent)
    
    reddit_tech = scrape_reddit_tech()
    # news.update(reddit_tech[1])
    
    reddit_world_news = scrape_reddit_world_news()
    # news.update(reddit_world_news[1])

    # Create a macro string with all the scraped news for the .txt file
    write_string += eurogamer[0] + '\n'
    write_string += wccftech[0] + '\n'
    write_string += bbc_news[0] + '\n'
    write_string += science_mag[0] + '\n'
    # reddit_instance = praw.Reddit(client_id = cred.client_id, client_secret = cred.client_secret, user_agent = cred.user_agent)
    write_string += reddit_tech[0] + '\n'
    write_string += reddit_world_news[0] + '\n'

    # Format the HTML string with the scraped information
    html_string += eurogamer[1] + '\n\t\t<p class="top-anchor"><a href="#page-top">Page Top</a></p>\n'
    html_string += wccftech[1] + '\n\t\t<p class="top-anchor"><a href="#page-top">Page Top</a></p>\n'
    html_string += bbc_news[1] + '\n\t\t<p class="top-anchor"><a href="#page-top">Page Top</a></p>\n'
    html_string += science_mag[1] + '\n\t\t<p class="top-anchor"><a href="#page-top">Page Top</a></p>\n'
    html_string += reddit_tech[1] + '\n\t\t<p class="top-anchor"><a href="#page-top">Page Top</a></p>\n'
    html_string += reddit_world_news[1] + '\n\t\t<p class="top-anchor"><a href="#page-top">Page Top</a></p>\n'

    # Finish the HTML in the html string
    html_string += '''\n\t\t</body>
    
</html>'''

    # After scraping the websites, write the information to a .txt file
    with open(file_name+'.txt', 'w') as f:
        f.write(write_string)
        # startfile(file_name+'.txt')
    
    # Write the scraped information to an HTML file
    with open(file_name+'.html','w') as f:
        f.write(html_string)
        startfile(file_name+'.html')

    # Output the elapsed time since the beginning of the script and the writing to the file
    print('Your news have been scraped.\nElapsed time:', round(time() - start_time, 3), 'seconds.')

    '''    
    # Prompt the user to enter 2 space-separated words
    print('Which news article should I open?')
    # open_news = input('Enter two space-separated words that appear in the title of the article: ').lower().split()

    # Run this loop while the user input is not empty
    while open_news:
        # Loop through the key-value pairs in the 'news' dictionary
        for key in news:
            # If both words are in a news' title, open the link of that news in the browser
            if open_news[0] in key.lower() and open_news[1] in key.lower():
                # Open the matched news' URL on the browser
                webbrowser.open(news[key])
                print('The news article has been opened in your default browser.')
                # If there was match, there's no need to keep looping through the dictionary
                break
        
        # If we finished looping through the dictionary, it means there was no match
        else:
            print('Your input did not match any title.')

        print()

        # Prompt the user for which news article to open next
        open_news = input('Enter two space-separated words that appear in the title of the article: ').lower().split()

    # Print a final statement after the user enters empty input
    else:
    '''

    print('The program has finished.')