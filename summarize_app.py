#!/usr/bin/env python

from flask import Flask, render_template, request

app = Flask(__name__)
import text_summarization


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/summarize', methods=["POST"])
def summarize():
    to_summarize = request.form['toSummarize']
    summary = text_summarization.generate_summary(3, to_summarize)
    print(summary)
    return str(summary)


app.run()
