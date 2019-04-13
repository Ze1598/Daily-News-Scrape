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
# Used to create a conection to a SMPT server
# import smtplib
# API used to connect to Gmail and send emails
import yagmail
# File with credentials for the Reddit API
import Ze1598Bot_credentials as cred
# Used to open URLs in the default browser
# import webbrowser

def scrape_eurogamer ():
	"""
	Scrape Eurogamer.net today's news.
	"""

	return_data = [['Eurogamer.net:\n'], []]
	target = get('http://www.eurogamer.net')
	soup = BeautifulSoup(target.content, 'html5lib')

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

		return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank"><span class="remove-anchor-style">{title}</span></a></li>')

	return return_data


def scrape_wccftech ():
	"""
	Scrape Wccftech's top 6 featured news.
	"""

	return_data = [['Wccftech:\n'], []]
	target = get('https://wccftech.com/')
	soup = BeautifulSoup(target.content, 'html5lib')

	for i in range(1,7):
		article = soup.find('a', class_='featured featured-'+str(i))
		title = article.h2.text
		url = article['href']
		return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank"><span class="remove-anchor-style">{title}</span></a></li>')

	# Scrape the first news from the Hardware, the Gaming and the Mobile sections
	# These are simply the first articles located in different <div> elements (\
	# nested inside unordered lists), where the <div> class is the item of the\
	# Python list we loop through
	for article in ["sticky-hardware", "sticky-gaming", "sticky-mobile"]:
		title = soup.find('section', class_=article).find('li', class_="first").h3.a.text.strip()
		url = soup.find('section', class_=article).find('li', class_="first").h3.a["href"].strip()
		return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank"><span class="remove-anchor-style">{title}</span></a></li>')

	return return_data


def scrape_jornal_noticias ():
	"""
	Scrape Jornal de Notícias.net today's news.
	"""

	return_data = [['Jornal de Notícias:\n'], []]
	target = get('https://www.jn.pt')
	soup = BeautifulSoup(target.content, 'html5lib')

	for article in soup.find_all('article', class_ = 't-g1-l1-am1'):
		url = 'https://www.jn.pt' + str(article.header.h2.a['href'])
		title = article.header.h2.text.strip()
		return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank"><span class="remove-anchor-style">{title}</span></a></li>')

	return return_data


def scrape_bbc_news ():
	"""
	Scrape the top 6 featured news from BBC World News.
	"""

	return_data = [['BBC World News:\n'], []]
	target = get('http://www.bbc.com/news/world')
	soup = BeautifulSoup(target.content, 'html5lib')

	# Article at the top
	top_article = soup.find('div', class_="buzzard-item")
	title = top_article.a.h3.text.strip()
	url = 'http://www.bbc.com' + top_article.a['href'].strip()
	return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank"><span class="remove-anchor-style">{title}</span></a></li>')


	# First and second columns (each contains a single news article)
	column = soup.find_all('div', class_='pigeon__column pigeon__column--a')
	for article in column:
		title = article.a.h3.text.strip()
		url = 'http://www.bbc.com' + article.a['href'].strip()
		return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank"><span class="remove-anchor-style">{title}</span></a></li>')
	
	# Third column (contains 3 news)
	column = soup.find('div', class_='pigeon__column pigeon__column--b').find_all('div', class_='pigeon-item faux-block-link')
	for article in column:
		title = article.a.h3.text.strip()
		url = 'http://www.bbc.com' + article.a['href'].strip()
		return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank"><span class="remove-anchor-style">{title}</span></a></li>')
	
	return return_data


def scrape_science_mag ():
	"""
	Scrape the first page of Latest News from Science Magazine.
	"""

	return_data = [['Science Magazine:\n'], []]
	target = get('http://www.sciencemag.org/')
	soup = BeautifulSoup(target.content, 'html5lib')

	# Extract the part of the HTML containing the articles to scrape
	articles = soup.find('ul', class_='tabbed__panel tabbed__grid').find_all('li')
	for post in articles:
		title = post.article.h2.a.text.strip()
		url = 'http://www.sciencemag.org' + post.article.h2.a['href']
		return_data[1].append(f'\n\t\t\t<li><a href="{url}" target="_blank"><span class="remove-anchor-style">{title}</span></a></li>')

	return return_data


def scrape_reddit_science ():
	"""
	Scrape the fist 7 posts in r/ science's Hot section 
	using Reddit's API.
	"""

	return_data = [['r/ Science:\n'], []]
	subreddit_instance = reddit_instance.subreddit('science')

	first_n_hot = list(subreddit_instance.hot(limit=7))
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data



def scrape_reddit_tech ():
	"""
	Scrape the fist 7 posts in r/ technology's Hot section 
	using Reddit's API.
	"""

	return_data = [['r/ Technology:\n'], []]
	subreddit_instance = reddit_instance.subreddit('technology')

	first_n_hot = list(subreddit_instance.hot(limit=9))
	# Delete subreddit-specific posts
	del first_n_hot[0:2]
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data


def scrape_reddit_world_news ():
	"""
	Scrape the fist 8 posts in r/ worldnews's Hot section
	using Reddit's API.
	"""

	return_data = [['r/ WorldNews:\n'], []]
	subreddit_instance = reddit_instance.subreddit('worldnews')

	first_n_hot = list(subreddit_instance.hot(limit=8))
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data 


def scrape_reddit_eli5 ():
	"""
	Scrape the fist 7 posts in r/ explainlikeimfive's 
	Hot section using Reddit's API.
	"""

	return_data = [['r/ ExplainLikeI\'mFive:\n'], []]
	subreddit_instance = reddit_instance.subreddit('explainlikeimfive')

	first_n_hot = list(subreddit_instance.hot(limit=6))
	# Delete subreddit-specific posts
	del first_n_hot[0]
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data


def scrape_reddit_til ():
	"""
	Scrape the fist 7 posts in r/ todayilearned's Hot section
	using Reddit's API.
	"""

	return_data = [['r/ TodayILearned:\n'], []]
	subreddit_instance = reddit_instance.subreddit('todayilearned')

	first_n_hot = list(subreddit_instance.hot(limit=5))
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data


def scrape_reddit_python ():
	"""
	Scrape the fist 5 posts in r/ Python's Hot section
	using Reddit's API.
	"""

	return_data = [['r/ Python:\n'], []]
	subreddit_instance = reddit_instance.subreddit('Python')

	first_n_hot = list(subreddit_instance.hot(limit=9))
	# Delete subreddit-specific posts
	del first_n_hot[0:2]
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data


def scrape_reddit_learn_prog ():
	"""
	Scrape the fist 5 posts in r/ learnprogramming's Hot section
	using Reddit's API.
	"""

	return_data = [['r/ learnprogramming:\n'], []]
	subreddit_instance = reddit_instance.subreddit('learnprogramming')

	first_n_hot = list(subreddit_instance.hot(limit=9))
	# Delete subreddit-specific posts
	del first_n_hot[0:2]
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data


def scrape_reddit_educational_gifs ():
	"""
	Scrape the fist 5 posts in r/ educationalgifs' Hot section
	using Reddit's API.
	"""

	return_data = [['r/ educationalgifs:\n'], []]
	subreddit_instance = reddit_instance.subreddit('educationalgifs')

	first_n_hot = list(subreddit_instance.hot(limit=5))
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data


def scrape_reddit_wallpapers ():
	"""
	Scrape the fist 10 posts in r/ wallpapers' Hot section
	using Reddit's API.
	"""

	return_data = [['r/ wallpapers:\n'], []]
	subreddit_instance = reddit_instance.subreddit('wallpapers')

	first_n_hot = list(subreddit_instance.hot(limit=10))
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data


def scrape_reddit_coolguides ():
	"""
	Scrape the fist 10 posts in r/ coolguides' Hot section
	using Reddit's API.
	"""

	return_data = [['r/ coolguides:\n'], []]
	subreddit_instance = reddit_instance.subreddit('coolguides')

	first_n_hot = list(subreddit_instance.hot(limit=10))
	for post in first_n_hot:
		return_data[1].append(f'\n\t\t\t<li><a href="{post.url}" target="_blank"><span class="remove-anchor-style">{post.title}</span></a></li>')

	return return_data


def scrape_xkcd (img_file=False):
	"""
	Scrape the latest comic (image file) and description from xkcd.com.

	Parameters
	---------
	img_file : bool
		True if the function should return an <img> element with the comic
		itself; else returns a <li> element with the comic's title as an
		anchor to the comic's URL.
	"""
	
	original_target = "https://xkcd.com"
	target = "https://xkcd.com/info.0.json"
	get_comic = get(target).json()
	img_source = get_comic["img"]
	img_title = get_comic["safe_title"]
	img_desc = get_comic["alt"]

	# If we want to display the comic itself in the page, then return an <img>\
	# HTML element with the comic's .png file
	if (img_file == True):
		article_html = f"\n\t\t\t<img src={img_source} id='xkcd-comic' />"
		# Return a tuple: the first item is the HTML to be used for the xkcd comic\
		# article; the second item is the title of the comic (a normal string); the\
		# third item is the comic URL
		return (article_html, img_title, img_source)
	# If we just want a reference to the comic, return a <li> element
	else:
		return f'\n\t\t\t<li><a href="{original_target}" target="_blank"><span class="remove-anchor-style">xkcd: {img_title}</span></a></li>'


def scrape_bluechair ():
	'''
	Scrape the URL for the latest Bluechair web comic.
	'''

	target = get("https://www.webtoons.com/en/comedy/bluechair/list?title_no=199")
	soup = BeautifulSoup(target.content, "html5lib")
	# All the comics (of the first page) are located inside a <div> with a class\
	# `detail_lst`
	comics_list = soup.find("div", class_="detail_lst")

	# Both the title and the comic's URL are, in the context of previous <div>,\
	# located inside the first <ul>, then inside the first <li> (since we want the\
	# most recent comic), then inside the first <a>

	# Inside that <a> element, the title is in the <span> with a class `subj`
	comic_title = comics_list.ul.li.a.find("span", class_="subj").span.text.strip()
	# The title is the value of the <a>'s `href` attribute
	comic_url = comics_list.ul.li.a["href"]
	

	return f'\n\t\t\t<li><a href="{comic_url}" target="_blank"><span class="remove-anchor-style">Bluechair: {comic_title}</span></a></li>'


def scrape_web_comics ():
	'''
	Function responsible for calling the necessary functions to scrape web comics.
	This function by itself doesn't do any scraping, only organizes what is scraped,
	in the regards of web comics.

	Parameters
	----------
	None

	Returns
	-------
	return_data : list
		A two-list list: the first list contains the title for the news section
		in the website; each item in the section list is a <li> HTML element,
		which corresponds to a single web comic.
	'''

	return_data = [['Web Comics:\n'], []]
	scrape_comics_funcs = [scrape_xkcd, scrape_bluechair]
	return_data[1] = [scrape_comics_func() for scrape_comics_func in scrape_comics_funcs]

	return return_data


def send_emails(email_subject, email_body):
	"""
	Send an email via Gmail with scraped news to a specified
	email account.

	Arguments
	---------
	email_subject : string
		The email subject.
	email_body : string
		A string of HTML with the email content (body).
	"""

	# Who will receive the email
	receiver = "jose.fernando.costa.1998@gmail.com"
	# Create a secure connection using an SMTP server
	yag = yagmail.SMTP("z.devtest.costa@gmail.com")
	# Send the email
	yag.send(
		to=receiver,
		subject=email_subject,
		contents=email_body
	)
	print(f'Your email has been sent to {receiver}.')
	return None


def main():
	# Get today's date
	today = date.today()
	# Get the current hour
	hour = datetime.now().hour

	# Define the name of the file to be written
	if hour < 12:
		full_date = f'{today}_{hour}AM_news'
	elif hour >= 12:
		full_date = f'{today}_{hour-12}PM_news'

	file_name_parts = full_date.split("_")
	news_time = f"{file_name_parts[0]} - {file_name_parts[1]} News"

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
			<h2 class="date">{news_time}</h2>
		</header>
		<nav id="nav-buttons">'''

	# Used to keep track of the number of references included in the HTML so far\
	# (for the top navigation menu)
	ref_counter = 0
	# Loop through a list of the names of the websites scraped to create the top\
	# navigation menu for the page
	for website in ["Web Comics", "Wccftech", "BBC World News", "r/ Science", "r/ Technology", "r/ WorldNews", "r/ Python", "r/ learnprogramming", "r/ educationalgifs", "r/ ExplainLikeI'mFive","r/ coolguides"]:
		# If it's the first website, then open a new <div> for making the reference
		if ref_counter == 0:
			html_string += "\n\t\t\t<div id='column1'>"
			html_string += f"\n\t\t\t\t\t<p class='section-nav-button'><a href='#{website}'><span class='remove-anchor-style'>{website}</span></a></p>"
		# Every four references we need to open a new <div>
		elif ref_counter%5 == 0:
			html_string += f"\n\t\t\t<div id='column{str(int(ref_counter/5)+1)}'>"
			html_string += f"\n\t\t\t\t\t<p class='section-nav-button'><a href='#{website}'><span class='remove-anchor-style'>{website}</span></a></p>"
		else:
			html_string += f"\n\t\t\t\t\t<p class='section-nav-button'><a href='#{website}'><span class='remove-anchor-style'>{website}</span></a></p>"
		# Starting at the fourth (index 3) reference, every four references we need to close\
		# a <div>
		if ref_counter in range(4, 50, 5):
			html_string += "\n\t\t\t</div>"
		
		# Increment the reference counter
		ref_counter += 1
	# Close the navigation menu
	html_string += '''\n\t\t\t<div class="clear" />
		</nav>'''


	# HTML to be used for the email to be sent
	mail_html_string = f'''<!DOCTYPE html>
<html>
	<head>
		<title>Daily News Scrape</title>
		<style>
			body {{
				font-family:Lato,sans-serif; 
				font-size: 175%;
				font-weight: bold;				
				width:70%;
			}}
		</style>
	</head>
	<body>
	<h1>Daily News Scrape</h1>
	<h2>{news_time}</h2>
	'''

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

	# List of functions to be called/websites to be scraped
	websites_list = [
				scrape_web_comics, scrape_bbc_news,
				scrape_reddit_science, scrape_reddit_tech, 
				scrape_reddit_world_news, scrape_reddit_educational_gifs,
				scrape_reddit_python, scrape_reddit_learn_prog,
				scrape_reddit_coolguides, scrape_wccftech,
				scrape_reddit_eli5
	]

	'''
	# Before scraping all the websites for news, scrape xkdc.com individually\
	# given that the result will be an image, not a list of news titles
	scraped_xkcd = scrape_xkcd()
	# Create the HTML for the .html file
	html_string += f"\n\n\t<article id=\"xkcd\" title=\"{scraped_xkcd[1]}\">{scraped_xkcd[0]}\n\t\t</article>"
	# Add the "Page Top" anchor
	html_string += "\n\t\t<p class=\"top-anchor\"><a href=\"#page-top\">Page Top</a></p>\n"
	# Create the HTML for the email body
	mail_html_string += f"\n\t\t<h3>xkcd</h3>\n\t\t\t<ul><li><a href=\"{scraped_xkcd[2]}\">{scraped_xkcd[1]}</a></li></ul>"
	'''

	# Loop through the list of functions (in other words, scrape each\
	# website)
	for website in websites_list:

		# Call the function
		scraped_data = website()
        
		# Create the beginning of the <article>
		html_string += f'''\n\n\t\t<article id="{scraped_data[0][0][:-2]}">
			<ul type="none">'''
		# Make a title for the email body for the current website
		mail_html_string += f'''\n\t\t<h3>{scraped_data[0][0][:-2]}</h3>
			<ul>'''

		# Loop through the list of news scraped from the current website
		# Since each item is a string already in HTML form, it can be added\
		# directly into the HTML string for the file and for the email
		for news in scraped_data[1]:
			html_string += news
			mail_html_string += news

		# Close the <article>
		html_string += '''\n\t\t\t</ul>
		</article>
		<p class="top-anchor"><a href="#page-top"><span class="remove-anchor-style">Page Top</span></a></p>\n'''
		# Close the list of news for the current website
		mail_html_string += '''\n\t\t</ul>'''

	# There's nothing more to add to the page, so close the <body> and\
	# end the file (</html>) for both HTMLs
	html_string += '''\n\t\t</body>

</html>'''
	
	# Finish off the HTML for the email body
	mail_html_string += '''\n\t</body>

</html>'''
	
	file_name = "Daily News Scrape"
	# Write the scraped information to an HTML file
	with open(file_name+'.html','wb') as f:
		'''
		# Encode the HTML string to ISO-8859-1, ignoring any encoding errors.
		# Since the encoding returns a bytes object, the file needs to be opened\
		# in binary read-write access mode
		# f.write(html_string.encode("ISO-8859-1", errors="ignore"))
		'''
		f.write(html_string.encode("ISO-8859-1", errors="ignore"))
    
	# Send the scraped news via email
	# The first argument is the email subject and the second is the email body\
	# (the HTML created using the `mail_html_string` variable)
	send_emails(news_time, mail_html_string)

	# Start the HTML file (open it in the computer's default browser)
	startfile(file_name+'.html')

	print('Your news have been scraped.')

	return None


if __name__ == '__main__':
	# Time how long it takes to run the script
	start_time = time()

	# Create a Reddit instance for API access
	reddit_instance = praw.Reddit(client_id=cred.client_id, client_secret=cred.client_secret, user_agent=cred.user_agent)

	# Call the main script to function to scrape data from the various\
	# websites, and write the information to an .html file. It is also\
	# responsible for calling the function responsible for sending an\
	# email with the information
	main()

	# Output the elapsed time since the beginning of the script and the writing to the file
	print('Elapsed time:', int(time() - start_time), 'seconds.')
	print('The program has finished.')