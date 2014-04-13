import pygoogle
import tweepy
#okay so what do i want to do
#get tweets. that return some music data rigth haha

# getting the lexicon

def getPartOfWord(word):
	string = ''
	for ch in word:
		if ch.isalpha():
			string += ch
		else:
			break
	return string

def readEmotionLookUpTable(location, sentimentlexicon): #sentimentlexicon is a string to int dictionary
	f = open(location)
	lines = f.readlines()
	f.close()
	# sentimentlexicon = {}
	for line in lines:
		parts = line.split()
		sentimentlexicon[getPartOfWord(parts[0])] = int(parts[1])
	return sentimentlexicon

def extractTweets(api):
	user = api.me()
	timeline = api.user_timeline(screen_name=user, include_rts=True, count=100)
	def created_at(item):
		return item.created_at
	return sorted(timeline, key=created_at)

def strip(word):
	string = ''
	for ch in word:
		if ch.isalpha():
			string += ch
		else:
			string += ' '
	return string

def isYoutube(url):
	if 'youtube' in url:
		return True
	else:
		return False

def getPlaylist(user, sortedtweets, mood, p): #returns a (user, mood, newsongslist) tuple
	playlist = []
	#get latest p tweets
	tweettexts = [x.text for x in sortedtweets[-p:]]
	#use a filtered list of sentiment terms from text + mood
	for text in tweettexts:
		words = [strip(x) for x in text.split()]
		searchterm = mood
		for word in words:
			if word in sentimentlexicon:
				searchterm += ' ' + word
		print 'searching for: ' + searchterm
		if len(searchterm) > 0:
			search = pygoogle.pygoogle(searchterm)
			urls = [x for x in search.get_urls() if isYoutube(x)]
			playlist += urls
	return playlist

def giveSong(user, sortedtweets, mood, p): #returns a (user, mood, newsongslist) tuple
	#get latest p tweets
	tweettexts = [x.text for x in sortedtweets[-p:]]
	#use a filtered list of sentiment terms from text + mood
	for text in tweettexts:
		words = [strip(x) for x in text.split()]
		searchterm = mood
		for word in words:
			if word in sentimentlexicon:
				searchterm += ' ' + word
		print 'searching for: ' + searchterm
		if len(searchterm) > 0:
			search = pygoogle.pygoogle(searchterm)
			urls = [x for x in search.get_urls() if isYoutube(x)]
			if len(urls) > 0:
				return urls[0]

	#just use sentiment terms 
	#first search for all the terms in the text
	#second search for all terms in the text appended with mood
	#third search for 
	# search = pygoogle.pygoogle(searchterm)#'it\'s too late to say im sorry')
	# test = search.get_urls()
	# searchterm = ''
	# if 'info' in mood:
	# 	#do informative search

	# else:
	# searchterm = mood

sentimentlexicon = readEmotionLookUpTable('lexicons/EmotionLookupTable.txt', {})
auth = tweepy.OAuthHandler(code1, code2)
auth.set_access_token(code3, code4)

api = tweepy.API(auth)

user = api.me()

print 'user ' + str(user)
print 'screen_name ' + str(user.screen_name)
print 'followers_count ' + str(user.followers_count)
print giveSong(api.me(), extractTweets(api), '', 10)
