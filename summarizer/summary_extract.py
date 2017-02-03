from re import split as regex_split, sub as regex_sub, UNICODE as REGEX_UNICODE
from collections import Counter
from math import fabs

from .utils import STOPWORDS

MIN_KEYWORD_LENGTH = 15
IDEAL = 20.0


def split_sentences(text):
    '''
    splites a sentence using regex
    '''    
    sentences = regex_split(u'(?<![A-ZА-ЯЁ])([.!?]"?)(?=\s+\"?[A-ZА-ЯЁ])', text, flags=REGEX_UNICODE)
    s_iter = zip(*[iter(sentences[:-1])] * 2)
    s_iter = [''.join(map(lambda x: x.strip(), y)).lstrip() for y in s_iter]
    s_iter.append(sentences[-1])
    return s_iter


def split_words(text):
    #split a string into array of words
    try:
        text = regex_sub(r'[^\w ]', '', text, flags=REGEX_UNICODE)  # strip special chars
        return [x.strip('.').lower() for x in text.split()]
    except TypeError:
        print("Error while splitting words")
        return None


def keywords(text):
    """
    get the top 15 words
    """
    text = split_words(text)
    num_of_words = len(text) 
    freq = Counter(x for x in text if x not in STOPWORDS)

    min_size = min(MIN_KEYWORD_LENGTH, len(freq)) 
    keywords_ = {x: y for x, y in freq.most_common(min_size)}

    for k in keywords_:
        article_score = keywords_[k]*1.0 / num_of_words
        keywords_[k] = article_score * 1.5 + 1

    return keywords_


def title_score(title, sentence):
    '''
    adds all the words from sentence present in title and 
    then divides the sum(occurances)/len(title)
    '''
    title = [x for x in title if x not in STOPWORDS]
    count = 0.0
    for word in sentence:
        if (word not in STOPWORDS and word in title):
            count += 1.0
            
    if len(title) == 0:
        return 0.0
        
    return count/len(title)


def length_score(sentence):
    '''
    normalzie a sentence's score
    '''
    return 1 - fabs(IDEAL - len(sentence)) / IDEAL


def dbs(words, keywords):
    if (len(words) == 0):
        return 0

    summ = 0
    first = []
    second = []

    for i, word in enumerate(words):
        if word in keywords:
            score = keywords[word]
            if first == []:
                first = [i, score]
            else:
                second = first
                first = [i, score]
                dif = first[0] - second[0]
                summ += (first[1]*second[1]) / (dif ** 2)

    # number of intersections
    k = len(set(keywords.keys()).intersection(set(words))) + 1
    return (1/(k*(k+1.0))*summ)


def sbs(words, keywords):
    score = 0.0
    if len(words) == 0:
        return 0
    for word in words:
        if word in keywords:
            score += keywords[word]
    return (1.0 / fabs(len(words)) * score)/10.0


def sentence_position(i, size):
    """
    different sentence position might indicate variness
    in importance
    """
    normalized = i*1.0 / size
    if 0 < normalized <= 0.1:
        return 0.17
    elif 0.1 < normalized <= 0.2:
        return 0.23
    elif 0.2 < normalized <= 0.3:
        return 0.14
    elif 0.3 < normalized <= 0.4:
        return 0.08
    elif 0.4 < normalized <= 0.5:
        return 0.05
    elif 0.5 < normalized <= 0.6:
        return 0.04
    elif 0.6 < normalized <= 0.7:
        return 0.06
    elif 0.7 < normalized <= 0.8:
        return 0.04
    elif 0.8 < normalized <= 0.9:
        return 0.04
    elif 0.9 < normalized <= 1.0:
        return 0.15
    else:
        return 0


def score(sentences, title_words, keywords):
    """
    score sentences based on different features
    """
    sentence_size = len(sentences)
    ranks = Counter()
    for i, s in enumerate(sentences):
        sentence = split_words(s)
        title_feature = title_score(title_words, sentence)
        sentence_length = length_score(sentence)
        sentence_pos = sentence_position(i+1, sentence_size)
        sbs_feature = sbs(sentence, keywords)
        dbs_feature = dbs(sentence, keywords)
        frequency = (sbs_feature + dbs_feature) / 2.0 * 10.0

        #weighted average of scores from four categories
        total_score = (title_feature*1.5 + frequency*2.0 +
                      sentence_length*1.0 + sentence_pos*1.0) / 4.0
        ranks[s] = total_score
    return ranks


def summarize(title, text):
    summaries = []
    sentences = split_sentences(text)
    keys = keywords(text)
    title_words = split_words(title)

    if len(sentences) <= 5:
        return sentences

    #score setences, and use the top 5 sentences
    ranks = score(sentences, title_words, keys).most_common(6)
    for rank in ranks:
        summaries.append(rank[0])

    return summaries
