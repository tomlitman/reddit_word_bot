# pycharm says this isnt in use, but it 100% is. so do not delete.
import Words
from pprint import pprint
import praw
import requests
import json
import string

reddit = praw.Reddit('word_bot', user_agent='Mac OS:WordBotv0.1 (by /u/J_Dymond)')
subreddit = reddit.subreddit('AbsolutelyNormal')

# gets top definition of word,
def get_def(word):

	# for OED API
	app_id = '5c9096e2'
	app_key = '50c202c6ebe0c06fc6beee5bf49fe152'
	language = 'en'
	word_id = word
	url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()
	r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})

	# code = 200, means the word is in the dictionary
	if r.status_code != 200:
		return ''

	# below is json for word info, un comment to see the data structure
	# print("text \n" + r.text)

	word_info = json.loads(r.text)['results']

	word_definitions = word_info[0]['lexicalEntries'][0]['entries'][0]['senses']

	# this bit gets the top definition, it's kind of fucked due to the formatting of the request result
	# probably need to rewrite, but atm isn't returning an error
	while True:
		try:
			def1 = word_definitions[0]['definitions'][0]
			break
		except KeyError:
			try:
				def1 = word_definitions[0]['subsenses'][0]['definitions'][0]
			except KeyError:
				def1 = word_definitions[0]['crossReferenceMarkers'][0]
			break

	reply = ('>' + word + ': \n\n ' + def1 + '\n\n')

	# ^^ all of this must have an easier solution, maybe traversing the json ^^
	#    rather than using specific guesses

	return reply

# gets words from a comment, puts them into an array, removes punctuation
def get_words(comment):
    comment_words = []
    for word in comment.split():
        exclude = set(string.punctuation)
        word = ''.join(ch for ch in word if ch not in exclude)
        comment_words.append(word)
    return comment_words

# if word is in relevant list, will return true.
def word_search(word):

	#Words starting with numbers exits function
	
	while True:
		try:
			char = int(word[0])
		except ValueError:
			break
			
		return False
	
	# lazily gets the relevant word list from Words.py, by using the first letter in the word.
	
	# this skips to the 2nd character of word if it's surrounded by quotation marks " 'be' " was raising an error
	# this only raises a syntax error from OEDs definition strings, as they somehow don't get stripped
	
	try:
		word_list = eval('Words.' + str.lower(word[0]))
	except SyntaxError:
		word_list = eval('Words.' + str.lower(word[1]))
	
	return word in word_list
    

def FindAndReply(submission):

	submission.comment_sort = 'new'

	submission.comments.replace_more(limit=0)
	for comment in submission.comments.list():

		Comment_Words = get_words(comment.body)
		
		for word in Comment_Words:

			if word_search(word) == True:
				reply = (get_def(word))
				print(reply)
			
				#comment.reply(reply)
				
				break
    

for submission in subreddit.hot(limit=10):

	 print(submission.title)  # Output: the submission's title
	 print(submission.id)     # Output: the submission's ID 
	 FindAndReply(submission)

