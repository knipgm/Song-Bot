import tweepy
import spotipy
import json
import time
from json.decoder import JSONDecodeError
from spotipy.oauth2 import SpotifyOAuth

#spotify keys
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = ""

#twitter keys
consumer_key = ""
consumer_secret = ""

key = ""
secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)




# read from tweet history file
def read_tweetHist(file):
    file_read = open(file, "r")
    tweet_id = int(file_read.read().strip())
    file_read.close()
    return tweet_id


# write to tweet history file
def store_tweetHist(file, tweet_id):
    file_write = open(file, "w")
    file_write.write(str(tweet_id))
    file_write.close()
    return

#searches for song and returns song URI
def searchForSong(text):
    CACHE = ".cache-" + "test"
    SCOPE = ''
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
           SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,scope = SCOPE,cache_path=CACHE
        )
    )

    searchResult = sp.search(text,1,0,"track")
    #print(json.dumps(searchResult,sort_keys=True,indent=4))

    songURI = searchResult['tracks']['items'][0]['uri']
    return songURI

def playSong(songID):
    CACHE = ".cache-" + "test"
    SCOPE = 'user-modify-playback-state'
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
           SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI,scope = SCOPE,cache_path=CACHE
        )
    )

    sp.add_to_queue(songID,None)
    return

def update():
    file = "Twitter Spotify Bot\\tweetHist.txt"
    tweets = api.mentions_timeline(read_tweetHist(file), tweet_mode="extended")

    for tweet in reversed(tweets):  # goes through all tweets that mention our bot
        # print (tweet)
        if "#request" in tweet.full_text.lower():
            store_tweetHist(file, tweet.id)
            print(str(tweet.id) + " - " + tweet.full_text)
            text = tweet.full_text.split('#request ')
            api.update_status(
            status="Thankyou, playing: "+text[1]+" next",
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True,)
            playSong(searchForSong(text[1]))
            
        

count = 0
while True:
    update()
    count+=1
    print('update: '+str(count))
    time.sleep(10)

