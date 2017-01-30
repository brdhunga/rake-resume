import os

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        job_description = request.form["description"]
        
        return render_template("results.html")
    return render_template('index.html')


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port, debug=True)