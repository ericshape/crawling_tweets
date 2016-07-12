from twitterOauth import *
import sys
import json

inputFileName=sys.argv[1]
start=int(sys.argv[2])
userIds = None
with open(inputFileName,'r') as inputFile:
    userIds = inputFile.readlines()

numUserIds = len(userIds)
with open(inputFileName+'_tweets_'+str(start),'w') as outputFile:
    for i in range(numUserIds):
        if (i<start):
            continue
#         userId = str(long(userIds[i]))
        userId = userIds[i].strip()
        allTweetsOfCurrentUser = [userId]
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+userId+'&count=200'
        content,rawContent = getValidJson(url)
        if content:
            allTweetsOfCurrentUser.append(rawContent)
            if len(content)>2 and 'id' in content[-1]:
                maxId = content[-1]['id']
                maxId -= 1
                for j in range(15):
                    sys.stdout.write('\r part %d done'%j)
                    sys.stdout.flush()
                    url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+userId+'&count=200&max_id='+str(maxId)
                    content,rawContent = getValidJson(url)
                    if content is None or len(content)==0:
                        break
                    allTweetsOfCurrentUser.append(rawContent)
                    if 'created_at' not in content[-1] or not content[-1]['created_at'].endswith('2014'):
                        break
                    if len(content)>2 and 'id' in content[-1]:
                        maxId = content[-1]['id']
                        maxId -= 1
                    else:
                        break
            else:
                continue
        else:
            print 'Request for user',userId,'failed.'
        if len(allTweetsOfCurrentUser)>1:
            for content in allTweetsOfCurrentUser:
                outputFile.write(content+'\n')
            outputFile.flush()
        sys.stdout.write('\r %d/%d done     \n'%(i,numUserIds))
        sys.stdout.flush()





