from re import split as regex_split, sub as regex_sub, UNICODE as REGEX_UNICODE
from collections import Counter

from .utils import STOPWORDS

MIN_KEYWORD_LENGTH = 15


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
    title = [x for x in title if x not in STOPWORDS]
    count = 0.0
    for word in sentence:
        if (word not in STOPWORDS and word in title):
            count += 1.0
            
    if len(title) == 0:
        return 0.0
        
    return count/len(title)
