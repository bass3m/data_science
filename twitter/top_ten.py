import sys
import json

# initialize term sentiment dict
hash_dict = {}

def get_hashtags(hashtag_lst):
    """ 
    Returns a list of hashtags, eliminating non alphanumeric chars
    hashtags: is an array of dicts with "text" and "indices" keys
    hashtags is in entities key
    """
    return [h['text'].lower().replace(' ','%20').encode('utf-8') for h in hashtag_lst]

def process_hashtags(tweets):
    """
    Returns term sentiment given the json'd tweets
    """
    for tw in tweets:
        if tw.has_key(u'lang') and tw[u'lang'] == u'en':
            hash_tags = get_hashtags(tw['entities']['hashtags'])
            for tag in hash_tags:
                hash_dict[tag] = hash_dict.get(tag,0) + 1

def parse_raw_tweets(raw_tweets_file):
    """
    Returns list containing json'd tweets
    """
    all_tweets = raw_tweets_file.readlines()
    return (json.loads(raw_tweet) for raw_tweet in all_tweets)

def get_word_frequency(word):
    """
    Never have to worry about divide by zero, since we must
    have at least 1 tweet. That means deno can never be zero.
    """
    return float(word_dict[word])/float(sum_words())

def main():
    tweet_file = open(sys.argv[1])
    process_hashtags(parse_raw_tweets(tweet_file))
    sorted_hashtags = sorted(hash_dict,
                             cmp=lambda x,y : hash_dict[x] - hash_dict[y],
                             reverse=True)
    for tag in xrange(0,10 if len(sorted_hashtags) > 10 else len(sorted_hashtags)):
        print "%s %.3f" % (sorted_hashtags[tag].replace(' ', '%20').encode('utf-8'),
                           float(hash_dict[sorted_hashtags[tag]]))

if __name__ == '__main__':
    main()
