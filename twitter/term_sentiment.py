import sys
import json

scores = {}

def make_term(pos_tws=0,neg_tws=0,total_pos=0,total_neg=0):
    return {'pos_tws'   : pos_tws, 'neg_tws'     : neg_tws,
            'total_pos' : total_pos, 'total_neg' : total_neg}

# initialize term sentiment dict
term_dict = {}

def sum_sentiments(tweet_words):
    return sum([scores.get(w,0) for w in tweet_words])

def get_tweet_words(tweet):
    """ 
    Returns a list of words, eliminating non alphanumeric chars
    """
    return [w.lower() for w in tweet.split(" ") if w.isalpha()]

def process_term_sentiment(tweets):
    """
    Returns term sentiment given the json'd tweets
    """
    for tw in tweets:
        if tw.has_key(u'lang') and tw[u'lang'] == u'en':
            words = get_tweet_words(tw['text'])
            sentiment_sum = sum_sentiments(words)
            is_pos = sentiment_sum >= 0
            for word in words:
                if not scores.has_key(word):
                    term_entry = term_dict.setdefault(word,make_term())
                    if is_pos is True:
                        term_entry['pos_tws'] = term_entry.get('pos_tws') + 1
                        term_entry['total_pos'] = term_entry.get('total_pos') + sentiment_sum
                    else:
                        term_entry['neg_tws'] = term_entry.get('neg_tws') + 1
                        term_entry['total_neg'] = term_entry.get('total_neg') + sentiment_sum

def parse_raw_tweets(raw_tweets_file):
    """
    Returns list containing json'd tweets
    """
    all_tweets = raw_tweets_file.readlines()
    return (json.loads(raw_tweet) for raw_tweet in all_tweets)

def parse_sentiment_file(sent_file):
    """
    Populate score dict containing sentiment values
    """
    for line in sent_file:
        term, score  = line.split("\t")
        scores[term] = int(score)

def get_term_avg(term):
    """
    Never have to worry about divide by zero, since we must
    have at least 1 tweet. That means deno can never be zero.
    """
    return float(term_dict[term]['total_pos'] + term_dict[term]['total_neg']) / \
            float(term_dict[term]['pos_tws'] + term_dict[term]['neg_tws'])

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    parse_sentiment_file(sent_file)
    process_term_sentiment(parse_raw_tweets(tweet_file))
    for term in term_dict.iterkeys():
        print "%s %.3f" %(term.replace(' ', '%20').encode('utf-8'),get_term_avg(term))

if __name__ == '__main__':
    main()
