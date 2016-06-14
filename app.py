from __future__ import unicode_literals
import os
from flask import Flask, request, jsonify

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 5

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    return "OK"


@app.route('/summarize', methods=['POST'])
def summarize():
    url = request.json.get('url')
    summary = summarize_url(url)
    return jsonify(summary)


def summarize_url(url):
    # E.G. url = "http://www.cnn.com/2016/06/12/politics/hillary-clinton-bernie-sanders-meeting-tuesday/index.html"
    print 'Summarizing ', url
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    print summarizer

    sentences = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print sentence
        sentences.append(str(sentence))

    return sentences


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", '0.0.0.0')
    app.run(host='0.0.0.0', port=port)
