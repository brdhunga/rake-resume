import os
from collections import OrderedDict

from flask import Flask, render_template, request, redirect, url_for

from rake import Rake, text
from summarizer import summarize


app = Flask(__name__)


def turn_tuple_to_dict(tuples):
	dict_ = OrderedDict()
	for tuple_ in tuples:
		dict_[tuple_[0]] = tuple_[1]
	return dict_


def flatten_values(input_):
    '''
    finds single words in keys of a dictionary
    e.g. dict_ = {"man in moon": 3, "what's this: 5", "bivu": 4}
    ["what's", 'this', 'bivu', 'man', 'in', 'moon']
    '''
    if type(input_) == dict:
        list_to_parse = input_.keys()
    else:
        list_to_parse = input_
    final_word_list = []
    for each_ in list_to_parse:
        final_word_list += list(map(lambda x: x.strip(), each_.split(" ")))
    return final_word_list



def get_common_words(keywords, sentences):
    '''
    get words that are comming using both rake and NLTK
    keywords is a dictinary 
    sentences is a list of sentences
    '''
    words_from_keywords = flatten_values(keywords)
    words_from_summaries = flatten_values(sentences)
    return [element for element in words_from_keywords if element in words_from_summaries]


@app.route('/', methods=['GET', 'POST'])
def index():
        if request.method == "POST":

                job_description = request.form["description"]
                job_title = request.form["title"]
                
                rake = Rake("all_stop_words.txt")
                keyword_tuples = rake.run(job_description)
                keyword_dict = turn_tuple_to_dict(keyword_tuples)
                
                important_sentences = summarize(job_title, job_description) 
                
                common_words = get_common_words(keyword_dict, important_sentences)                
               
                return render_template("results.html", 
                                    keywords=keyword_dict, 
                                    summaries=important_sentences,
                                    common_words = common_words)

        return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)