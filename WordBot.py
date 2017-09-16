import praw
import requests
import json
from pprint import pprint

#for OED API
app_id = '5c9096e2'
app_key = '50c202c6ebe0c06fc6beee5bf49fe152'

from urllib.parse import quote_plus

reddit = praw.Reddit('word_bot', user_agent='Mac OS:WordBotv0.1 (by /u/J_Dymond)')

subreddit = reddit.subreddit('AbsolutelyNormal')


# for submission in subreddit.hot(limit=10):
#     print(submission.title)  # Output: the submission's title
#     print(submission.score)  # Output: the submission's score
#     print(submission.id)     # Output: the submission's ID 
    
submission = reddit.submission(id='70cc44')
submission.comment_sort = 'new'

for top_level_comment in submission.comments:
    body = top_level_comment.body
    print(body)
    if 'Awry' in body:
    	language = 'en'
    	word_id = 'Awry'
    	url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()
    	r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})
    	
    	#print("text \n" + r.text)
    	WordInfo = json.loads(r.text)['results']
    	
    	WordDefinitions = WordInfo[0]['lexicalEntries'][0]['entries'][0]['senses']
    	
    	def1 = WordDefinitions[0]['definitions'][0]
    	def2 = WordDefinitions[0]['subsenses'][0]['definitions'][0]
    	
    	reply = ('Awry: \n\n1) ' + def1 + '\n\n2)' + def2)
    	top_level_comment.reply(reply)
    	
    	break