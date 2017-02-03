from re import split as regex_split, sub as regex_sub, UNICODE as REGEX_UNICODE


def split_sentences(text):
    '''
    splites a sentence using regex
    '''    
    sentences = regex_split(u'(?<![A-ZА-ЯЁ])([.!?]"?)(?=\s+\"?[A-ZА-ЯЁ])', text, flags=REGEX_UNICODE)
    s_iter = zip(*[iter(sentences[:-1])] * 2)
    s_iter = [''.join(map(lambda x: x.strip(), y)).lstrip() for y in s_iter]
    s_iter.append(sentences[-1])
    return s_iter


