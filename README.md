# Daily-News-Scrape

A simple project that uses a Python script to scrape news titles and their URLs from various websites, then writes the information to a .txt and an .html file.

### Future Updates:
I expect to keep updating this repo over time, as I make changes to the page's style and add/update news sources.

### Update log:

* (may 27th 2018) Updated the script to scrape news from more sources. I've also commented out the option to write the news to a .txt file, so now running the script only outputs the .html file (hence the difference in dates in the 2 example files uploaded to ther repo).

* (nov 20th 2018) Updated the script code's to be cleaner and more streamlined. I also updated the page's style and a added a couple of new news sources. Along with these changes I uploaded an example file to showcase what type of file the Python scripts creates now.

* (jan 3rd 2019) Updated the main script to further automate the creation of HTML and the code, in general, more modular and easier to edit. I also added the functionality to send the scraped news via email, through Gmail; Lastly, I added one or two new news sources, and changed the order of appearance for some websites.

* (jan 13th 2019) Updated the main script with the ability to scrape the latest comic from xkcd.com (the .png file URL), along with some new changes to the page's CSS.

* (jan 24th 2019) Updated the first news section to be "Web Comics" instead, which will be used to link to the latest web comics of select sources (xkcd and Bluechair for now); also largely updated the color scheme and background for the whole page

* (feb 26th 2019) Updated the page with a couple of new news sources. I also changed the order of the news slightly.


### External references:

* Most recent example of the repo running on CodePen: https://codepen.io/ze1598/pen/rPNbdq

* Beautiful Soup (Handle Markup in Python): https://www.crummy.com/software/BeautifulSoup/bs4/doc/

* Requests (Make REST requests): http://docs.python-requests.org/en/master/

* praw (The Python Reddit API Wrapper): https://github.com/praw-dev/praw

* yagmail (Send emails through Gmail): https://pypi.org/project/yagmail/

* Background image: https://images.pexels.com/photos/860379/pexels-photo-860379.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940