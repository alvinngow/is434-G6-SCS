import praw
import pandas as pd
import numpy as np
import advertools as adv
from prawcore.exceptions import Forbidden

# api
reddit = praw.Reddit(client_id='EQlR29dhRQlv4Y31BZspAA',
                     client_secret='ae7DSXt0nDCYzqsWuhkVTrlCVJLq1g', user_agent='school-related')

conditions = ["depression", "ptsd", "anxiety"]
# , "bipolar","schizophrenia", "ocd", "paranoia", "anorexia", "psychosis"]

params = {'sort': 'new', 'limit': None, 'syntax': 'cloudsearch'}
# posts with "mental health" in title in r/Singapore

allPost = pd.DataFrame()
noOfPosts = []

# retrieve information about posts
for condition in conditions:
    posts = []
    posts_about_mental_health = reddit.subreddit(
        "Singapore").search(condition, **params)

    for post in posts_about_mental_health:
        posts.append([post.title, post.score, post.id, post.subreddit, post.url,
                      post.num_comments, post.selftext, post.created, post.author])

    posts = pd.DataFrame(posts, columns=[
        'title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'author'])

    noOfPosts.append({condition: len(posts)})
    # print(posts_about_mental_health)

# print(noOfPosts)
