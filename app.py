from __future__ import unicode_literals
import os
from flask import Flask, render_template, request, jsonify

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer as TextSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer as ESummarizer
from sumy.summarizers.kl import KLSummarizer as KLSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer as LexSummarizer
from sumy.summarizers.lsa import LsaSummarizer as LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer as LuhnSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer as SumBasicSummarizer


from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
nltk.data.path.append('./nltk_data/')

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
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    print dir(request)
    print request.json
    url = request.json.get('url')
    summarizer = request.json.get('summarizer')
    summary = summarize_url(url,summarizer)
    return jsonify(summary)


def summarize_url(url,summarizer):
    # E.G. url = "http://www.cnn.com/2016/06/12/politics/hillary-clinton-bernie-sanders-meeting-tuesday/index.html"
    print 'Summarizing ', url
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    if summarizer == 'luhn':
        summarizer = LuhnSummarizer(stemmer)
    elif summarizer == 'edmundson':
        summarizer = ESummarizer(stemmer)
    elif summarizer == 'lsa':
        summarizer = LsaSummarizer(stemmer)
    elif summarizer == 'lex':
        summarizer = LexRankSummarizer(stemmer)
    elif summarizer == 'text':
        summarizer = TextRankSummarizer(stemmer)
    elif summarizer == 'sb':
        summarizer = SumBasicSummarizer(stemmer)
    elif summarizer == 'kl':
        summarizer = KLSummarizer(stemmer)
        
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
    app.run(host=host, port=port)
