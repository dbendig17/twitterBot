import tweepy
import time

print('This is my twitter bot');

CONSUMER_KEY = 'Ko6GucIlpIdtgyorIcMkXPyLW'
CONSUMER_SECRET = '046BGhBwLgu7SGBt0kC1YsnhbELfBcxwwcg0zoTvyzoQKRw3c6'
ACESS_KEY = '1169674505242992641-CG7KJf9fPYeNm8xszGcP8YvdpAEHUZ'
ACESS_SECRET = 'ydMQItmd7AMlAKflnhUq2zRd9V1rQzapOPtvCaFzsMVlm'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACESS_KEY, ACESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

user = api.me()

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets ...')
    # for testing, first tweet id is: 1256387027416887296
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode = 'extended')

    for mention in reversed(mentions):
        print(str(mention.id) + ' -- ' + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        print('Liking mention ...')
        api.create_favorite(mention.id)
        if '#hello' in mention.full_text.lower():
            print('Found #hello!')
            print('responding back ...')
            api.update_status('#hello back to you ' + '@' + mention.user.screen_name, mention.id)
        if '#goodmorning' in mention.full_text.lower():
            print('Found #goodmorning!')
            print('responding back ...')
            api.update_status('@' + mention.user.screen_name + ' Good morning, have a nice day!', mention.id)
        if '#retweet' in mention.full_text.lower():
            print('Found #retweet!')
            print('retweet ...')
            api.retweet(mention.id)

def follow_followers():
    for follower in tweepy.Cursor(api.followers).items():
        try:
            follower.follow()
            print('follower: ' + follower.name)
        except tweepy.error.TweepError:
            #print('Already following user.')
            pass

follow_followers()
while True:
    reply_to_tweets()
    time.sleep(60)
