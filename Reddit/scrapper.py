import matplotlib.pyplot as plt
import praw
import pandas as pd
import numpy as np
import advertools as adv
from prawcore.exceptions import Forbidden


conditions = ["depression", "ptsd", "anxiety", "bipolar",
              "schizophrenia", "ocd", "paranoia", "anorexia", "psychosis"]
lenArray = []

noOfPosts = []
total = 0
allPost = pd.DataFrame()


# api
reddit = praw.Reddit(client_id='EQlR29dhRQlv4Y31BZspAA',
                     client_secret='ae7DSXt0nDCYzqsWuhkVTrlCVJLq1g', user_agent='school-related')


params = {'sort': 'new', 'limit': None, 'syntax': 'cloudsearch'}


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
    return my_autopct


print("retrieving")

# retrieve information about posts
for condition in conditions:
    print(condition)
    posts = []
    # search for post
    posts_about_mental_health = reddit.subreddit(
        "Singapore").search(condition, **params)

    for post in posts_about_mental_health:
        posts.append([post.title, post.score, post.id, post.subreddit, post.url,
                      post.num_comments, post.selftext, post.created, post.author])

    posts = pd.DataFrame(posts, columns=[
        'title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'author'])

    length = len(posts)
    noOfPosts.append({condition: length})
    lenArray.append(length)
    total += len(posts)
    # print(posts_about_mental_health)

explodeArr = []

for e in range(len(lenArray)):
    explodeArr.append(0.1)


x = np.array(lenArray)
plt.pie(x, labels=conditions, autopct=make_autopct(x), explode=explodeArr)
plt.legend(conditions, bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
plt.show()
