from bs4 import BeautifulSoup
import urllib.request

# gets all words wrapped in <i> tags from the page. will only work on urls from the islandnet domain.
def word_getter(letter):

    # gets the html for the 'a' page.
    page = urllib.request.urlopen('http://islandnet.com/~egbird/dict/'+letter+'.htm')

    # parses page into BeautifulSoup object
    soup = BeautifulSoup(page, 'html.parser')

    # finds all strings contained in <i> tags and puts them in ResultSet object
    raw_list = soup.find_all('i')

    words = []

    # iterates through ResultSet, converts into a str, removes tags and everything after whitespace, leaving only the word.
    for x in raw_list:

        # the letters indicate the regex that worked for them on the site.
        # unfortunately this had to be done manually, to figure out how each page was styled.
        # should be able to optimise this process at some point.

        # a-c, i, m, n
        words.append(str(x).split(" ")[0][3:])
        # d-h, j-l, o, p, s-v, x-z
        #words.append(str(x).split(" ")[0][4:].strip("\t-"))
        # q, r
        # words.append(str(x).split(" ")[1][7:].split("\t")[0])
        # w
        # words.append(str(x).split(" ")[1][6:].split("\"")[0])

    return words