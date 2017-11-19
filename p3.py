## SI 206 2017
## Project 3
## Building on HW7, HW8 (and some previous material!)

##THIS STARTER CODE DOES NOT RUN!!


##OBJECTIVE:
## In this assignment you will be creating database and loading data
## into database.  You will also be performing SQL queries on the data.
## You will be creating a database file: 206_APIsAndDBs.sqlite

import unittest
import itertools
import collections
import tweepy
import json
import sqlite3

## Your Name: Sydney Hunt
## The name of anyone you worked with on this project:

#####

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = "tSSmjXj2wUuJfFqneE1UylDfo"
consumer_secret = "Nalv8aGz8Hx4m5gzb25jx4xl8nDQcbll8EClfAz5LJXi5ri98K"
access_token = "464846788-UlDBvt3WK7bjxbRyhjDjG6Prw6eMxFxEIRnGTAFj"
access_token_secret = "7ZboZQwEpqJbJ5XfmW9wJ696m22zYLq0Oa8EsWkG5Xh1R"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON format
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

##### END TWEEPY SETUP CODE

## Task 1 - Gathering data

## Define a function called get_user_tweets that gets at least 20 Tweets
## from a specific Twitter user's timeline, and uses caching. The function
## should return a Python object representing the data that was retrieved
## from Twitter. (This may sound familiar...) We have provided a
## CACHE_FNAME variable for you for the cache file name, but you must
## write the rest of the code in this file.

CACHE_FNAME = "206_APIsAndDBs_cache.json"

# Put the rest of your caching setup here:
try:
    cache_file = open(CACHE_FNAME,'r') #opens file, reads file
    cache_contents = cache_file.read() #converts to str
    cache_file.close() #closes file
    CACHE_DICTION = json.loads(cache_contents) #loads content to dictionary
except:
    CACHE_DICTION = {}

# Define your function get_user_tweets here:

def get_user_tweets(user):
	if user in CACHE_DICTION:
		print("Using Cached Data")
		return CACHE_DICTION[user]
	else:
		print("Getting Data From Internet")
		final = api.user_timeline(id = user, count = 21)
		CACHE_DICTION[user] = final
		file1 = open(CACHE_FNAME,'w')
		file1.write(json.dumps(CACHE_DICTION))
		file1.close
	return final

# Write an invocation to the function for the "umich" user timeline and
# save the result in a variable called umich_tweets:

umich_tweets = get_user_tweets("@umich")

## Task 2 - Creating database and loading data into database
## You should load into the Users table:
# The umich user, and all of the data about users that are mentioned
# in the umich timeline.
# NOTE: For example, if the user with the "TedXUM" screen name2 is
# mentioned in the umich timeline, that Twitter user's info should be
# in the Users table, etc.

conn = sqlite3.connect('206_APIsAndDBs.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('''CREATE TABLE "Users" ("user_id" TEXT PRIMARY KEY NOT NULL UNIQUE,"screen_name" TEXT,"num_favs" INTEGER,"description" TEXT)''',)

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('''CREATE TABLE "Tweets" ("tweet_id" TEXT PRIMARY KEY NOT NULL UNIQUE,"var3" TEXT,"user_posted" TEXT,"time_posted" DATETIME,"retweets" INTEGER,FOREIGN KEY (user_posted) REFERENCES Users(user_id))''')

for user1 in umich_tweets:
	id1 = user1['user']['id']
	name1 = user1['user']['screen_name']
	favorites1 = user1['user']['favourites_count']
	user_description1 = user1['user']['description']
	mention1 = user1['entities']['user_mentions']
	var2 = (id1, name1, favorites1, user_description1)
	cur.execute('INSERT or IGNORE INTO Users (user_id, screen_name, num_favs, description) VALUES(?, ?, ?, ?)', var2)

	for items in mention1:
		name2 = items['screen_name']
		var2 = api.get_user(name2)
		cur.execute('INSERT OR IGNORE INTO Users (user_id, screen_name, num_favs, description) VALUES (?,?,?,?)', (var2["id_str"], var2["screen_name"], var2["favourites_count"], var2["description"]))

for tweet1 in umich_tweets:
	id2 = tweet1['id_str']
	var3 = tweet1['text']
	user2 = tweet1['user']['id']
	created1 = tweet1['created_at']
	retweets = tweet1['retweet_count']
	var4 = (id2, var3, user2, created1, retweets)
	cur.execute('INSERT INTO Tweets (tweet_id, var3, user_posted, time_posted, retweets) VALUES(?, ?, ?, ?, ?)', var4)

conn.commit()


## You should load into the Tweets table:
# Info about all the tweets (at least 20) that you gather from the
# umich timeline.
# NOTE: Be careful that you have the correct user ID reference in
# the user_id column! See below hints.


## Task 3 - Making queries, saving data, fetching data

# All of the following sub-tasks require writing SQL statements
# and executing them using Python.

users_info = []
cur.execute('SELECT * FROM Users')
tot = cur.fetchall()
for x in tot:
	users_info.append(tuple(x))


screen_names = []
cur.execute('SELECT (screen_name) FROM Users')
x = cur.fetchall()
for y in x:
	screen_names.append(y[0])


retweets = []
cur.execute('SELECT * FROM Tweets WHERE retweets > 10')
y = cur.fetchall()
for x in y:
	retweets.append(x)

favorites = []
cur.execute('SELECT (description) FROM Users WHERE num_favs > 500')
for x in cur:
	print(favorites.append(x[0]))


joined_data = []
cur.execute('SELECT Users.screen_name, Tweets.var3 FROM Users INNER JOIN Tweets ON Users.user_id = Tweets.user_posted')
for x in cur:
	joined_data.append(x)


joined_data2 = []
cur.execute('SELECT Users.screen_name, Tweets.var3 FROM Users INNER JOIN Tweets ON Users.user_id = Tweets.user_posted ORDER BY Tweets.retweets DESC')
for y in cur:
	joined_data2.append(y)


### IMPORTANT: MAKE SURE TO CLOSE YOUR DATABASE CONNECTION AT THE END
### OF THE FILE HERE SO YOU DO NOT LOCK YOUR DATABASE (it's fixable,
### but it's a pain). ###

###### TESTS APPEAR BELOW THIS LINE ######
###### Note that the tests are necessary to pass, but not sufficient --
###### must make sure you've followed the instructions accurately!
######
print("\n\nBELOW THIS LINE IS OUTPUT FROM TESTS:\n")


class Task1(unittest.TestCase):
	def test_umich_caching(self):
		fstr = open("206_APIsAndDBs_cache.json","r")
		data = fstr.read()
		fstr.close()
		self.assertTrue("umich" in data)
	def test_get_user_tweets(self):
		res = get_user_tweets("umsi")
		self.assertEqual(type(res),type(["hi",3]))
	def test_umich_tweets(self):
		self.assertEqual(type(umich_tweets),type([]))
	def test_umich_tweets2(self):
		self.assertEqual(type(umich_tweets[18]),type({"hi":3}))
	def test_umich_tweets_function(self):
		self.assertTrue(len(umich_tweets)>=20)

class Task2(unittest.TestCase):
	def test_tweets_1(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=20, "Testing there are at least 20 records in the Tweets database")
		conn.close()
	def test_tweets_2(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[1])==5,"Testing that there are 5 columns in the Tweets table")
		conn.close()
	def test_tweets_3(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT tweet_id FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(result[0][0] != result[19][0], "Testing part of what's expected such that tweets are not being added over and over (tweet id is a primary key properly)...")
		if len(result) > 20:
			self.assertTrue(result[0][0] != result[20][0])
		conn.close()


	def test_users_1(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=2,"Testing that there are at least 2 distinct users in the Users table")
		conn.close()
	def test_users_2(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)<20,"Testing that there are fewer than 20 users in the users table -- effectively, that you haven't added duplicate users. If you got hundreds of tweets and are failing this, let's talk. Otherwise, careful that you are ensuring that your user id is a primary key!")
		conn.close()
	def test_users_3(self):
		conn = sqlite3.connect('206_APIsAndDBs.sqlite')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==4,"Testing that there are 4 columns in the Users database")
		conn.close()

class Task3(unittest.TestCase):
	def test_users_info(self):
		self.assertEqual(type(users_info),type([]),"testing that users_info contains a list")
	def test_users_info2(self):
		self.assertEqual(type(users_info[0]),type(("hi","bye")),"Testing that an element in the users_info list is a tuple")

	def test_track_names(self):
		self.assertEqual(type(screen_names),type([]),"Testing that screen_names is a list")
	def test_track_names2(self):
		self.assertEqual(type(screen_names[0]),type(""),"Testing that an element in screen_names list is a string")

	def test_more_rts(self):
		if len(retweets) >= 1:
			self.assertTrue(len(retweets[0])==5,"Testing that a tuple in retweets has 5 fields of info (one for each of the columns in the Tweet table)")
	def test_more_rts2(self):
		self.assertEqual(type(retweets),type([]),"Testing that retweets is a list")
	def test_more_rts3(self):
		if len(retweets) >= 1:
			self.assertTrue(retweets[1][-1]>10, "Testing that one of the retweet # values in the tweets is greater than 10")

	def test_descriptions_fxn(self):
		self.assertEqual(type(favorites),type([]),"Testing that favorites is a list")
	def test_descriptions_fxn2(self):
		self.assertEqual(type(favorites[0]),type(""),"Testing that at least one of the elements in the favorites list is a string, not a tuple or anything else")
	def test_joined_result(self):
		self.assertEqual(type(joined_data[0]),type(("hi","bye")),"Testing that an element in joined_result is a tuple")



if __name__ == "__main__":
	unittest.main(verbosity=2)
