from django.shortcuts import render
from google.cloud import language_v1
import tweepy
import re
# Create your views here.

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': {"Testvdvd", "trests s:tests s"}}
    return render(request, 'index2.html', context)


def transfer(request):
    print("request---", request.POST.get("name_field", ""))
    keyword = request.POST.get("name_field", "")
    scraped_data1 = gettweetusinftweepy(keyword)
    set1 = sample_analyze_sentiment_local(scraped_data1)
    # set1 = {"This is s a good oy  dfdffdfdfdfdfdfdfdfdfdfdfffdffddfdf fdfdf ":90,
    #         "This is a bad boy br":98,
    #         "This is a bad boy br ddd":98,
    #         "This is a bad boy br ddddd":78,
    # }
    context = {'latest_question_list': set1}
    return render(request, 'sentiment_analysis.html', context)


def sample_analyze_sentiment_local(text_content):
    set1 = set()
    dict_item = {}
    print("ALL VALUES IN SET END", set1)
    for val in text_content:
        magnitude = sample_analyze_sentiment_text(val)
        print("magnitude----------", magnitude)
        print("val----------", val)
        if magnitude is not None:
            magnitude = str(magnitude)
        if val is not None:
            val = str(val)
        if magnitude is not None and val is not None:
            total = val + " >>>>>>>>  " + magnitude
            print("total", total)
            set1.add(total)
            dict_item[val] = magnitude
    print("ALL VALUES IN SET END", set1)
    return dict_item


def sample_analyze_sentiment_text(text_content):
    client = language_v1.LanguageServiceClient()
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))
        return sentence.sentiment.score

    print(u"Language of the text: {}".format(response.language))


def gettweetusinftweepy(keyword):
    access_token = "1129086671394238464-KtjanDK7dONBCk2VAswPKGfR5CNJFE"
    access_token_secret = "JswcEJnO4TnjHmAiOUce7WEgaMut4Ex5QOGeAHC4Qued9"
    consumer_key = "tSosFRlMmLKGmqi5RckXI4shI"
    consumer_secret = "LUOhxgj6Yhb6T2OFMkWf1cYR2s2gikKtJvUtoATYWCUwI9dK6y"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    words = keyword
    scraped_data = set()
    print("Enter number of tweets to be scraped ")
    numtweet = 10
    scraped_data1 = scrape(words, numtweet, scraped_data, api)
    return scraped_data1


def scrape(words, numtweet, scraped_data, api):
    tweets = tweepy.Cursor(api.search_tweets, q=words, lang="en",
                           tweet_mode='extended').items(numtweet)
    list_tweets = [tweet for tweet in tweets]
    i = 1
    for tweet in list_tweets:
        username = tweet.user.screen_name
        description = tweet.user.description
        location = tweet.user.location
        following = tweet.user.friends_count
        followers = tweet.user.followers_count
        totaltweets = tweet.user.statuses_count
        # retweetcount = tweet.user.retweet_count
        hashtags = tweet.entities['hashtags']

        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        ith_tweet = [username, description, location, following,
                     followers, totaltweets, text, hashtext]
        printtweetdata(i, ith_tweet, scraped_data)
        i = i + 1
    scrap_data2 = set()
    for i in scraped_data:
        clean_data = re.sub(r'[^A-Za-z0-9 ]', '', i)
        scrap_data2.add(clean_data)
    return scrap_data2


def printtweetdata(n, ith_tweet, scraped_data):
    d = ith_tweet[6]
    scraped_data.add(d)
