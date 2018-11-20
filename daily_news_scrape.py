'''
Scrape news titles and its URLs from a set of websites then 
create an .html file and open it using the computer's 
default browser.
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

    return_data = [['Eurogamer.net:\n'], []]
    target = get('http://www.eurogamer.net').text
    soup = BeautifulSoup(target, 'html5lib')

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
        except:
            title = article.p.a.text.strip()

        return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>')

    return return_data


def scrape_wccftech():
    '''Scrape Wccftech's top 6 featured news.'''

    return_data = [['Wccftech:\n'], []]
    target = get('https://wccftech.com/').text
    soup = BeautifulSoup(target, 'html5lib')

    for i in range(1,7):
        article = soup.find('a', class_='featured featured-'+str(i))
        title = article.h2.text
        url = article['href']
        return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>')
    
    # Scrape the first news from the Hardware, the Gaming and the Mobile sections
    # These are simply the first articles located in different <div> elements (\
    # nested inside unordered lists), where the <div> class is the item of the\
    # Python list we loop through
    for article in ["sticky-hardware", "sticky-gaming", "sticky-mobile"]:
        title = soup.find('section', class_=article).find('li', class_="first").h3.a.text.strip()
        url = soup.find('section', class_=article).find('li', class_="first").h3.a["href"].strip()
        return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>')

    return return_data


def scrape_jornal_noticias():
    '''Scrape Jornal de Notícias.net today's news.'''

    return_data = [['Jornal de Notícias:\n'], []]
    target = get('https://www.jn.pt').text
    soup = BeautifulSoup(target, 'html5lib')

    for article in soup.find_all('article', class_ = 't-g1-l1-am1'):
        url = 'https://www.jn.pt' + str(article.header.h2.a['href'])
        title = article.header.h2.text.strip()
        return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>')

    return return_data


def scrape_bbc_news():
    '''Scrape the top 6 featured news from BBC World News.'''

    return_data = [['BBC World News:\n'], []]
    target = get('http://www.bbc.com/news/world').text
    soup = BeautifulSoup(target, 'html5lib')

    # Article at the top
    top_article = soup.find('div', class_="buzzard-item")
    title = top_article.a.h3.text.strip()
    url = 'http://www.bbc.com' + top_article.a['href'].strip()
    return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>')


    # First and second columns (each contains a single news article)
    column = soup.find_all('div', class_='pigeon__column pigeon__column--a')
    for article in column:
        title = article.a.h3.text.strip()
        url = 'http://www.bbc.com' + article.a['href'].strip()
        return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>')
    
    # Third column (contains 3 news)
    column = soup.find('div', class_='pigeon__column pigeon__column--b').find_all('div', class_='pigeon-item faux-block-link')
    for article in column:
        title = article.a.h3.text.strip()
        url = 'http://www.bbc.com' + article.a['href'].strip()
        return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>')

    return return_data


def scrape_science_mag():
    '''Scrape the first page of Latest News from Science Magazine.'''

    return_data = [['Science Magazine:\n'], []]
    target = get('http://www.sciencemag.org/').text
    soup = BeautifulSoup(target, 'html5lib')

    # Extract the part of the HTML containing the articles to scrape
    articles = soup.find('ul', class_='tabbed__panel tabbed__grid').find_all('li')
    for post in articles:
        title = post.article.h2.a.text.strip()
        url = 'http://www.sciencemag.org' + post.article.h2.a['href']
        return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank">{title}</a></li>')

    return return_data


def scrape_reddit_tech():
    '''Scrape the fist 10 posts in r/ technology's Hot section 
    using Reddit's API.'''

    return_data = [['r/ Technology:\n'], []]
    subreddit_instance = reddit_instance.subreddit('technology')
    
    first_n_hot = list(subreddit_instance.hot(limit=12))
    # Delete subreddit-specific posts
    del first_n_hot[0:2]
    for post in first_n_hot:
        return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank">{post.title}</a></li>')
    
    return return_data


def scrape_reddit_world_news():
    '''Scrape the fist 10 posts in r/ worldnews's Hot section
    using Reddit's API.'''

    return_data = [['r/ WorldNews:\n'], []]
    subreddit_instance = reddit_instance.subreddit('worldnews')

    first_n_hot = list(subreddit_instance.hot(limit=10))
    for post in first_n_hot:
        return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank">{post.title}</a></li>')

    return return_data 


def scrape_reddit_eli5():
    '''Scrape the fist 7 posts in r/ explainlikeimfive's 
    Hot section using Reddit's API.'''

    return_data = [['r/ ExplainLikeI\'mFive:\n'], []]
    subreddit_instance = reddit_instance.subreddit('explainlikeimfive')

    first_n_hot = list(subreddit_instance.hot(limit=6))
    # Delete subreddit-specific posts
    del first_n_hot[0]
    for post in first_n_hot:
        return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank">{post.title}</a></li>')

    return return_data


def scrape_reddit_til():
    '''Scrape the fist 7 posts in r/ todayilearned's Hot section
    using Reddit's API.'''

    return_data = [['r/ TodayILearned:\n'], []]
    subreddit_instance = reddit_instance.subreddit('todayilearned')

    first_n_hot = list(subreddit_instance.hot(limit=5))
    for post in first_n_hot:
        return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank">{post.title}</a></li>')

    return return_data


def scrape_reddit_python():
    '''Scrape the fist 5 posts in r/ Python's Hot section
    using Reddit's API.'''

    return_data = [['r/ Python:\n'], []]
    subreddit_instance = reddit_instance.subreddit('Python')

    first_n_hot = list(subreddit_instance.hot(limit=9))
    # Delete subreddit-specific posts
    del first_n_hot[0:2]
    for post in first_n_hot:
        return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank">{post.title}</a></li>')

    return return_data


def scrape_reddit_learn_prog():
    '''Scrape the fist 5 posts in r/ learnprogramming's Hot section
    using Reddit's API.'''

    return_data = [['r/ learnprogramming:\n'], []]
    subreddit_instance = reddit_instance.subreddit('learnprogramming')

    first_n_hot = list(subreddit_instance.hot(limit=9))
    # Delete subreddit-specific posts
    del first_n_hot[0:2]
    for post in first_n_hot:
        return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank">{post.title}</a></li>')

    return return_data


def scrape_reddit_educational_gifs():
    '''Scrape the fist 7 posts in r/ educationalgifs' Hot section
    using Reddit's API.'''

    return_data = [['r/ educationalgifs:\n'], []]
    subreddit_instance = reddit_instance.subreddit('educationalgifs')

    first_n_hot = list(subreddit_instance.hot(limit=7))
    for post in first_n_hot:
        return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank">{post.title}</a></li>')

    return return_data


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
    elif hour >= 12:
        file_name = f'{today}_{hour-12}PM_news'

    # The string to hold the HTML to be written to the file
    # This includes the whole <head> and the page's <header>
    html_string = f'''<!DOCTYPE html>
<html>
    <head>
        <title>Daily News Scrape</title>
        <meta charset="ISO-8859-1">
        <link rel="stylesheet" type="text/css" href="news.css">
    </head>
    
    <body>
        <header class="page-header" id="page-top">
            <h1 class="title">Daily News Scrape</h1>
            <h2 class="date">{today}</h2>
        </header>
        <nav id="nav-buttons">
        	<div id="column1">
        		<p class="section-nav-button"><a href="#Eurogamer.net">Eurogamer.net</a></p>
        		<p class="section-nav-button"><a href="#Wccftech">Wccftech</a></p>
        		<p class="section-nav-button"><a href="#Jornal de Notícias">Jornal de Notícias</a></p>
        		<p class="section-nav-button"><a href="#BBC World News">BBC World News</a></p>
        	</div>
        	
        	<div id="column2">
        		<p class="section-nav-button"><a href="#Science Magazine">Science Magazine</a></p>
        		<p class="section-nav-button"><a href="#r/ Technology">r/ Technology</a></p>
        		<p class="section-nav-button"><a href="#r/ WorldNews">r/ WorldNews</a></p>
        		<p class="section-nav-button"><a href="#r/ Python">r/ Python</a></p>
        	</div>

        	<div id="column3">
        		<p class="section-nav-button"><a href="#r/ learnprogramming">r/ learnprogramming</a></p>
        		<p class="section-nav-button"><a href="#r/ educationalgifs">r/ educationalgifs</a></p>
        		<p class="section-nav-button"><a href="#r/ ExplainLikeI'mFive">r/ ExplainLikeI'mFive</a></p>
        		<p class="section-nav-button"><a href="#r/ TodayILearned">r/ TodayILearned</a></p>
        	</div>

        	<div class="clear" />

        </nav>'''

    # Call each function to scrape data and save the returned\
    # results. Since the returned result for each function is a\
    # tuple where the first item is a string to be written to the\
    # file and the second is a mapping of the website's news\ 
    # titles and URLs, update the contents of that dictionary
    # to the 'news' dictionary.

    # Call each function to scrape data from a specific website.
    # Each function is responsible for scraping the news from one\
    # website and return a list of two items: (1) a string which is\
    # the name of the website and (2) a list of strings, where each\
    # string is a line of HTML about one scraped news post.
    # Since the same HTML structure is used to present the news from\
    # each website, we can use simplify the process: create the\
    # same beginning and end for each <article> (the content for each\
    # website), then, in the middle, fill it with the HTML parts\
    # returned by each function

    # Create a Reddit instance for API access
    reddit_instance = praw.Reddit(client_id = cred.client_id, client_secret = cred.client_secret, user_agent = cred.user_agent)
    websites_list = [scrape_eurogamer, scrape_wccftech, scrape_jornal_noticias, scrape_bbc_news,
    				scrape_science_mag, scrape_reddit_tech, scrape_reddit_world_news,
    				scrape_reddit_python, scrape_reddit_learn_prog, scrape_reddit_educational_gifs, 
    				scrape_reddit_eli5, scrape_reddit_til]

    # Loop through the list of functions (in other words, scrape each\
    # website)
    for website in websites_list:
    	# Call the function
        scraped_data = website()
        # Create the beginning of the <article>
        html_string += f'''\n\n\t\t<article id="{scraped_data[0][0][:-2]}">
            <ul type="none">'''
        for news in scraped_data[1]:
            html_string += news
        # Close the <article>
        html_string += '''\n\t\t\t</ul>
        </article>
        <p class="top-anchor"><a href="#page-top">Page Top</a></p>\n'''
    # There's nothing more to add to the page, so close the <body> and\
    # end the file (</html>)
    html_string += '''\n\t\t</body>
    
</html>'''

    # Write the scraped information to an HTML file
    with open(file_name+'.html','wb') as f:
    	# Encode the HTML string to ISO-8859-1, ignoring any encoding errors.
    	# Since the encoding returns a bytes object, we open the file in binary\
    	# read-write access mode
        f.write(html_string.encode("ISO-8859-1", errors="ignore"))
        # Start the HTML file (open it in the computer's default browser)
        startfile(file_name+'.html')

    # Output the elapsed time since the beginning of the script and the writing to the file
    print('Your news have been scraped.\nElapsed time:', int(time() - start_time), 'seconds.')
    print('The program has finished.')