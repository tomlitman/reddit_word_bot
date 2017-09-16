from pprint import pprint
import praw
import requests
import json
import string

# for OED API
app_id = '5c9096e2'
app_key = '50c202c6ebe0c06fc6beee5bf49fe152'

# I have no idea what this does, or if it's useful
# from urllib.parse import quote_plus

reddit = praw.Reddit('word_bot', user_agent='Mac OS:WordBotv0.1 (by /u/J_Dymond)')

subreddit = reddit.subreddit('AbsolutelyNormal')

# for submission in subreddit.hot(limit=10):
#     print(submission.title)  # Output: the submission's title
#     print(submission.score)  # Output: the submission's score
#     print(submission.id)     # Output: the submission's ID 

submission = reddit.submission(id='70cc44')
submission.comment_sort = 'new'


# gets top definition of word,
def get_def(word):
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


for top_level_comment in submission.comments:

    Words = get_words(top_level_comment.body)
    reply = ''

    # at the moment I'm singling out specific comments, by words that are specific to the comment
    if 'code' in Words:

        for word in Words:
            reply = reply + (get_def(word))

        top_level_comment.reply(reply)

        break
