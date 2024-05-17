import json
import pprint
from linkedin_api import Linkedin
from datetime import datetime
from datetime import date
import json
import os.path

linkedin = Linkedin("username", "password")
profile_id = "ashishtanwar"

def getTsFromPostId(post_id):
    link_ts = x=str(bin(int(post_id)))[2:43]
    return datetime.fromtimestamp(link_ts / 1e3)


def getPosts():

    # profile = linkedin.get_profile(profile_id)
    # profile["contact_info"] = linkedin.get_profile_contact_info(
    #     "ashishtanwar"
    # )
    #
    # print(profile)

    for i in range(100):
        posts=linkedin.get_profile_posts(profile_id,post_offset=i,post_count=i*100)

        # pprint.pp(posts)

        # print(posts)
        ts = date.today().strftime("%b-%d-%Y")
        with open("post"+ts+".log", 'w') as file:
            file.write(json.dumps(posts))
        
        for post in posts:
            post_urn = post['socialDetail']['urn'].split(":")[3]
            post_link= post['socialContent']['shareUrl']
            print ("Post Urn : %s, share : %s " %( post_urn,post_link))
            post_text = post['commentary']['text']['text']
        #   ts = post['commentary'][ '"publishedAt"']
            
            print(post_text)
            post_ts = getTsFromPostId(post_urn)
            print(post_ts)
        
    
def getComments():
    with open("postMay-13-2024.log", 'r') as file:
        posts = json.loads(file.read())

    for post in posts:
        post_urn = post['socialDetail']['urn'].split(":")[3]
    
        comments_file="comments"+post_urn+".log"
            #pprint.pp(comments)
        if os.path.isfile(comments_file) :
            print('Comments file exist, so skipping: '+comments_file)
            #skip
            continue
        
        print('Getting comments for post: '+ post['socialContent']['shareUrl'])
        
        comments = linkedin.get_post_comments(post_urn)
        
        with open(comments_file, 'w') as file:
                file.write(json.dumps(comments))

        for comment in comments:
            if not 'com.linkedin.voyager.feed.MemberActor' in comment['commenter']:
                continue

            commenter = comment['commenter']['com.linkedin.voyager.feed.MemberActor']['miniProfile']
            print("Commenter : "+commenter['firstName']+" "+ commenter['lastName'])
            print("Comment : "+str(comment['commentV2']))
            print("Time stamp : "+ str(comment['createdTime']))






# getPosts()
getComments()
