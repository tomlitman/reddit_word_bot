import praw

reddit = praw.Reddit(client_id='10f6M8u6wLvIiw',
                     client_secret='vv7nmiB8qdIneB5CzoILNan7-TM',
                     user_agent='Mac OS:WordBotv0.1 (by /u/J_Dymond)',
                     username='word_bot',
                     password='nibba123!')

subreddit = reddit.subreddit('SaintsFC')

#for submission in subreddit.hot(limit=10):
#    print(submission.title)  # Output: the submission's title
#    print(submission.score)  # Output: the submission's score
#    print(submission.id)     # Output: the submission's ID
#    print(submission.url) 
    
submission = reddit.submission(id='708wzq')
submission.comment_sort = 'new'
for top_level_comment in submission.comments:
    print(top_level_comment.body)


