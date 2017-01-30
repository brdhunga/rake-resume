# Implementation of RAKE - Rapid Automtic Keyword Exraction algorithm
# as described in:
# Rose, S., D. Engel, N. Cramer, and W. Cowley (2010). 
# Automatic keyword extraction from indi-vidual documents. 
# In M. W. Berry and J. Kogan (Eds.), Text Mining: Applications and Theory.unknown: John Wiley and Sons, Ltd.

                              
import re
import operator

debug = False
test = True


def is_number(s):
    try:
        float(s) if '.' in s else int(s)
        return True
    except ValueError:
        return False


def load_stop_words(stop_word_file):
    """
    Utility function to load stop words from a file and return as a list of words
    @param stop_word_file Path and file name of a file containing stop words.
    @return list A list of stop words.
    """
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    return stop_words


def separate_words(text, min_word_return_size):
    """
    Utility function to return a list of all words that are have a length greater than a specified number of characters.
    @param text The text that must be split in to words.
    @param min_word_return_size The minimum no of characters a word must have to be included.
    """
    splitter = re.compile('[^a-zA-Z0-9_\\+\\-/]')
    words = []
    for single_word in splitter.split(text):
        current_word = single_word.strip().lower()
        #leave numbers in phrase, but don't count as words, since they tend to invalidate scores of their phrases
        if len(current_word) > min_word_return_size and current_word != '' and not is_number(current_word):
            words.append(current_word)
    return words


def split_sentences(text):
    """
    Utility function to return a list of sentences.
    @param text The text that must be split in to sentences.
    """
    sentence_delimiters = re.compile(u'[.!?,;:\t\\\\"\\(\\)\\\'\u2019\u2013]|\\s\\-\\s')
    sentences = sentence_delimiters.split(text)
    return sentences


def build_stop_word_regex(stop_word_file_path):
    stop_word_list = load_stop_words(stop_word_file_path)
    stop_word_regex_list = []
    for word in stop_word_list:
        word_regex = r'\b' + word + r'(?![\w-])'  # added look ahead for hyphen
        stop_word_regex_list.append(word_regex)
    stop_word_pattern = re.compile('|'.join(stop_word_regex_list), re.IGNORECASE)
    return stop_word_pattern


def generate_candidate_keywords(sentence_list, stopword_pattern):
    phrase_list = []
    for s in sentence_list:
        tmp = re.sub(stopword_pattern, '|', s.strip())
        phrases = tmp.split("|")
        for phrase in phrases:
            phrase = phrase.strip().lower()
            if phrase != "":
                phrase_list.append(phrase)
    return phrase_list


def calculate_word_scores(phraseList):
    word_frequency = {}
    word_degree = {}
    for phrase in phraseList:
        word_list = separate_words(phrase, 0)
        word_list_length = len(word_list)
        word_list_degree = word_list_length - 1
        #if word_list_degree > 3: word_list_degree = 3 #exp.
        for word in word_list:
            word_frequency.setdefault(word, 0)
            word_frequency[word] += 1
            word_degree.setdefault(word, 0)
            word_degree[word] += word_list_degree  #orig.
            #word_degree[word] += 1/(word_list_length*1.0) #exp.
    for item in word_frequency:
        word_degree[item] = word_degree[item] + word_frequency[item]

    # Calculate Word scores = deg(w)/frew(w)
    word_score = {}
    for item in word_frequency:
        word_score.setdefault(item, 0)
        word_score[item] = word_degree[item] / (word_frequency[item] * 1.0)  #orig.
    #word_score[item] = word_frequency[item]/(word_degree[item] * 1.0) #exp.
    return word_score


def generate_candidate_keyword_scores(phrase_list, word_score):
    keyword_candidates = {}
    for phrase in phrase_list:
        keyword_candidates.setdefault(phrase, 0)
        word_list = separate_words(phrase, 0)
        candidate_score = 0
        for word in word_list:
            candidate_score += word_score[word]
        keyword_candidates[phrase] = candidate_score
    return keyword_candidates


class Rake(object):
    def __init__(self, stop_words_path):
        self.stop_words_path = stop_words_path
        self.__stop_words_pattern = build_stop_word_regex(stop_words_path)

    def run(self, text):
        sentence_list = split_sentences(text)

        phrase_list = generate_candidate_keywords(sentence_list, self.__stop_words_pattern)

        word_scores = calculate_word_scores(phrase_list)

        keyword_candidates = generate_candidate_keyword_scores(phrase_list, word_scores)

        sorted_keywords = sorted(keyword_candidates.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_keywords
    
text = '''
Minimum Required Skills:
JavaScript, JQuery, WordPress, CMS Based Websites, HTML, CSS, Git, Node.JS, Ruby On Rails, Visual / Graphic Design

Front End Developer needed for fast growing well established tech start up in East Memphis!! You must have experience bringing a teammate's designs to life, meaning you can take a flat design comp and transform it with engaging, thoughtful interactions. But don't stop there. We want you taking strong concepts and elevating them into jaw-dropping interactive experiences by suggesting weirdo stuff that only a great developer knows how to do. You would spend a lot of time building CMS-based websites for clients, so you will rely on tried-and-true platforms like Wordpress, Craft and all of the great e-commerce platforms. But, we want you empowered to push boundaries, consider alternate platforms and find new ways to solve old problems. We believe in the power of interactive design and development to do just about anything. You would be part of an adventurous crew that's willing to roll up their sleeves and figure things out, even when it seems impossible. HTML, CSS and JavaScript skills are must-haves. We prioritize code quality, semantics and browser performance, so you need to, too. We approach most websites mobile-first and take progressive enhancement seriously, so knowledge of device and browser limitations is a must.

Top Reasons to Work with Us

Great pay, Excellent benefits and Career growth!!

What You Will Be Doing

In Your First Week
• Meet your coworkers and learn how we work as a team.
• Review our current lineup of projects.
• Familiarize yourself with our systems and processes.
• Attend planning meetings for your first project.
• Start writing code.

In Your First Month
• Build a website from start to finish using Wordpress, Craft or another popular CMS.
• Collaborate with a designer to help realize their design.
• Document potential areas of improvement in your or the team's processes, focusing on efficiency and quality.

In Your First Three Months
• Get in the groove on building beautiful and efficient websites.
• Collaborate with other developers to create, document and adhere to a consistent workflow.
• Involve yourself in the design process to identify opportunities to elevate design and architecture through creative development solutions.
• Begin tinkering with our SaSS products in Ruby on Rails and Node.js.

Looking Ahead
• The basics of executing on a CMS site are easy, and now we have a process for getting it done quickly.
• Alongside client work, you're adding features and improving the UI of our full product lineup.
• You're focused on micro-interactions, animation and general badassery making our websites dynamic and world-class.

What You Need for this Position

• Able to write clean and semantic HTML and CSS
• Confident with JavaScript, not just jQuery
• Proficient with Git and other techniques for collaborative coding
• Comfortable using (or at least learning about) task runners, deployment automation and managing multiple environments
• Not scared by complicated problems

What's In It for You

Great pay, excellent benefits and career growth!!So, if you are a Front End Developer, please apply today!

Applicants must be authorized to work in the U.S.Please apply directly to by clicking 'Click Here to Apply' with your Word resume!

Looking forward to receiving your resume and going over the position in more detail with you.

- Not a fit for this position? Click the link at the bottom of this email to search all of our open positions.
'''

r = Rake("all_stop_words.txt")
