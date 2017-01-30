import os
from collections import OrderedDict

from flask import Flask, render_template, request, redirect, url_for

from rake import Rake, text


app = Flask(__name__)


def turn_tuple_to_dict(tuples):
	dict_ = OrderedDict()
	for tuple_ in tuples:
		dict_[tuple_[0]] = tuple_[1]
	return dict_


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":

        job_description = request.form["description"]
        rake = Rake("all_stop_words.txt")
        keyword_tuples = rake.run(job_description)
        keyword_dict = turn_tuple_to_dict(keyword_tuples)        
        return render_template("results.html", keywords=keyword_dict)

    return render_template('index.html')


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)