import oauth2 as oauth
import json
import time


API_KEY=[""]
API_SECRET=[""]
ACCESS_KEY=[""]
ACCESS_SECRET=[""]

NUM_KEYS=len(API_KEY)

def oauth_req(url, keyIndex,  http_method="GET", post_body=None,
        http_headers=None):
    consumer = oauth.Consumer(key=API_KEY[keyIndex], secret=API_SECRET[keyIndex])
    token = oauth.Token(key=ACCESS_KEY[keyIndex], secret=ACCESS_SECRET[keyIndex])
    client = oauth.Client(consumer, token)

    resp, content = client.request(
        url,
        method=http_method,
        body="",
        headers=http_headers,
    )
    return content

keyIndex = 0
def getValidJson(url):
    global keyIndex
    restart = True
    content = None
    while(restart):
        restart = False
        rawContent = oauth_req(url,keyIndex)
        content=json.loads(rawContent)
        if 'errors' in content:
            for error in content['errors']:
                if error['code']==88:
                    restart = True
                    keyIndex += 1
                    print 'Changing key to', keyIndex
                    if (keyIndex == NUM_KEYS):
                        keyIndex = 0
                        print 'Restart request after 100 seconds'
                        time.sleep(100)
                        break
                else:
                    print error
                    return None, rawContent
    return (content,rawContent)
