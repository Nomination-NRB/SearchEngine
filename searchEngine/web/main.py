# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, send_from_directory
from search_engine import SearchEngine
import xml.etree.ElementTree as ET
import sqlite3
import configparser
import jieba
from gensim.models import KeyedVectors
import jieba.posseg as pseg
import random

app = Flask(__name__)

doc_dir_path = ''
db_path = ''
page = []
keys = ''
checked = ['checked="true"', '', '']
origin = ''

config = configparser.ConfigParser()
config.read('../config.ini', 'utf-8')
mv_path = config['DEFAULT']['mv_path']
model = KeyedVectors.load_word2vec_format(mv_path, binary=False)


def init():
    config = configparser.ConfigParser()
    config.read('../config.ini', 'utf-8')
    global doc_dir_path, db_path, mv_path, model, stopwords
    doc_dir_path = config['DEFAULT']['doc_dir_path']
    db_path = config['DEFAULT']['db_path']
    stop_path = config['DEFAULT']['stop_words_path']
    with open(stop_path, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]


@app.route('/')
def main():
    init()

    return render_template('search.html', error=True)


@app.route('/search/', methods=['POST'])
def search():
    try:
        global keys, page, checked, origin, page, keywords
        page = []
        keys = request.form['key_word']
        keys = keys.replace(' ', '')
        if keys != '':
            keywords = jieba.cut(keys)
            words = pseg.lcut(keys)
            keywords = ' '.join(keywords)
            print(keywords)
            flag, page = searchidlist(keywords, 0)
            print(page)
            new_texts = []
            limit = 2
            nouns = [word for word, flags in words if flags.startswith('n') and word in model and word not in stopwords]
            print(nouns)
            # 将nouns转成字符串，若有多个名词，则空格分隔
            nouns = ' '.join(nouns)
            print(nouns)
            for i in range(5):
                if len(nouns) > limit:
                    selected_nouns = random.sample(nouns, limit)
                else:
                    selected_nouns = nouns
                new_words = []
                for word, flags in words:
                    if word in selected_nouns:
                        similar_words = model.most_similar(word)
                        new_word = similar_words[i][0]
                        while new_word in new_words:
                            new_word = similar_words[i + 1][0]
                            i = i + 1
                        new_words.append(new_word)
                    else:
                        new_words.append(word)
                new_text = ''.join(new_words)
                new_texts.append(new_text)

            if flag == 0:
                return render_template('search.html', key=keys, page=page, error=False)
            docs = cut_page(page, 0)
            return render_template('high_search.html', checked=checked, key=keywords, docs=docs, page=page,
                                   origin=origin, error=True, related_searches=new_texts)
        else:
            return render_template('search.html', key=keys, error=False)
    except:
        print('search error')
        return render_template('search.html', error=False)


@app.route('/search/<key>/', methods=['POST'])
def high_search(key):
    try:
        global keys, checked
        selected = int(request.form['order'])
        for i in range(3):
            if i == selected:
                checked[i] = 'checked="true"'
            else:
                checked[i] = ''
        keywords = jieba.cut(key)
        keywords = ' '.join(keywords)
        print(keywords)
        nouns = [word for word, flags in pseg.lcut(key) if flags.startswith('n') and word in model and word not in stopwords]
        print(nouns)
        # 将nouns转成字符串，若有多个名词，则空格分隔
        nouns = ' '.join(nouns)
        print(nouns)
        flag, page = searchidlist(keywords, selected)
        if flag == 0:
            return render_template('search.html', key=keys, page=page, error=False)
        docs = cut_page(page, 0)
        return render_template('high_search.html', checked=checked, key=keys, docs=docs, page=page, error=True)
    except:
        print('high search error')


def searchidlist(key, selected=0):
    global doc_id, doc_score, doc_score_2
    doc_id = []
    doc_score = []
    doc_score_2 = []
    se = SearchEngine('../config.ini', 'utf-8')
    flag, id_scores = se.search(key, selected)
    for docid, scores in id_scores:
        doc_id.append(docid)
        doc_score.append(scores[0])
        doc_score_2.append(scores[1])
    page = []
    for i in range(1, -(-len(doc_id) // 10) + 1):
        page.append(i)
    return flag, page


def cut_page(page, no):
    start = no * 10
    end = start + 10
    docs = find(doc_id[start:end])
    return docs


def find(docid, extra=False):
    docs = []
    for id in docid:
        root = ET.parse(doc_dir_path + '%s.xml' % id).getroot()
        url = root.find('url').text
        source = root.find('source').text
        title = root.find('title').text
        body = root.find('body').text
        id = int(id)
        score = doc_score_2[doc_id.index(id)]
        time = root.find('datetime').text.split(' ')[0]
        datetime = root.find('datetime').text
        doc = {'url': url, 'title': title, 'source': source, 'score': score, 'datetime': datetime,
               'time': time, 'body': body,
               'id': id, 'extra': []}
        if extra:
            temp_doc = get_k_nearest(db_path, id)
            for i in temp_doc:
                root = ET.parse(doc_dir_path + '%s.xml' % i).getroot()
                title = root.find('title').text
                doc['extra'].append({'id': i, 'title': title})
        docs.append(doc)
    return docs


@app.route('/search/page/<int:page_no>/', methods=['GET'])
def next_page(page_no):
    try:
        start = (page_no - 1) * 10
        end = start + 10
        docs = cut_page(page[start:end], (page_no - 1))
        return render_template('high_search.html', checked=checked, key=keys, docs=docs, page=page, error=True)
    except:
        print('next error')
        return render_template('high_search.html', checked=checked, key=keys, docs=[], page=page, error=True)


@app.route('/search/<id>/', methods=['GET', 'POST'])
def content(id):
    try:
        doc = find([id], extra=True)
        return render_template('content.html', doc=doc[0], key=keywords)
    except:
        print('content error')


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


def get_k_nearest(db_path, docid, k=5):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM knearest WHERE id=?", (docid,))
    docs = c.fetchone()
    conn.close()
    return docs[1: 1 + (k if k < 5 else 5)]


if __name__ == '__main__':
    jieba.initialize()
    app.run()
