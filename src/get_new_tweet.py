import requests
import os
from dotenv import load_dotenv


load_dotenv()

# Run Every 30s

# Get Recent Tweet from {user ID}
# https://api.twitter.com/2/tweets/search/recent?query=from%3AFF_XIV_JP
# https://api.twitter.com/2/tweets/search/recent?query=from%3A{user_id}
# return tweet_id

# Filter new tweets(update later)

# create new tweet URL
# https://twitter.com/FF_XIV_JP/status/1492306625918795776
# https://twitter.com/{user_id}/status/{tweet_id}

# Send to all sgroups
# Send message API (replyX)
# Send broadcast message

bearer_token = os.getenv("TWITTER_BEARER_TOKEN")


def get_single_tweet_url(user_id, tweet_id):
    return "https://twitter.com/{}/status/{}".format(user_id, tweet_id)


def create_url(user_id):
    url = "https://api.twitter.com/2/tweets/search/recent?query=from%3A{}".format(
        user_id
    )
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    print("bearer_token")
    print(bearer_token)

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    print("r")
    print(r)
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_recent_tweet(user_id):
    url = create_url(user_id)
    json_response = connect_to_endpoint(url)
    newest_id = json_response["meta"]["newest_id"]
    # filter new tweet
    return get_single_tweet_url(user_id, newest_id)


get_recent_tweet("FF_XIV_JP")
