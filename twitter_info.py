import tweepy

consumer_key = "tSSmjXj2wUuJfFqneE1UylDfo"
consumer_secret = "Nalv8aGz8Hx4m5gzb25jx4xl8nDQcbll8EClfAz5LJXi5ri98K"
access_token = "464846788-UlDBvt3WK7bjxbRyhjDjG6Prw6eMxFxEIRnGTAFj"
access_token_secret = "7ZboZQwEpqJbJ5XfmW9wJ696m22zYLq0Oa8EsWkG5Xh1R"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
