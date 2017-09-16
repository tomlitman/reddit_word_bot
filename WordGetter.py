from bs4 import BeautifulSoup
import urllib.request

# gets all words wrapped in <i> tags from the page. will only work on urls from the islandnet domain.

# gets the html for the 'a' page.
page = urllib.request.urlopen('http://islandnet.com/~egbird/dict/a.htm')

# parses page into BeautifulSoup object
soup = BeautifulSoup(page, 'html.parser')

# finds all strings contained in <i> tags and puts them in ResultSet object
raw_list = soup.find_all('i')

paragraphs = []

# iterates through ResultSet, converts into a str, removes tags and everything after whitespace, leaving only the word.
for x in raw_list:
    paragraphs.append(str(x).split(" ")[0][3:])
print(paragraphs)
