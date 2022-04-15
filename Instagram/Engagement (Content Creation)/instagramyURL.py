from instagramy import InstagramUser, InstagramHashTag
from instagramy.plugins.analysis import *
from instagramy.plugins.download import *

# Connecting the profile 
session_id = "52264498243%3AzMX2vsD89Jwplq%3A28"
user = InstagramUser("sgchildrensoc", sessionid=session_id) 

print(user.user_data)

tag = InstagramHashTag('sgchildrensoc', sessionid=session_id)
print(tag.posts_display_urls)