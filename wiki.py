import concurrent.futures
import itertools
import operator
import re
import constants as c
import requests
import wikipedia
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.summarization.bm25 import BM25
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, QuestionAnsweringPipeline
from googletrans import Translator
import os
import spacy
from flask import jsonify



class QueryProcessor:

    def __init__(self, nlp, keep=None):
        self.nlp = nlp
        self.keep = keep or {'PROPN', 'NUM', 'VERB', 'NOUN', 'ADJ'}

    def generate_query(self, text):
        doc = self.nlp(text)
        query = ' '.join(token.text for token in doc if token.pos_ in self.keep)
        return query


class DocumentRetrieval:

    def __init__(self, url='https://en.wikipedia.org/w/api.php'):
        self.url = url

    def search_pages(self, query):
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json'
        }
        res = requests.get(self.url, params=params)
        return res.json()

    def search_page(self, page_id):
        res = wikipedia.page(pageid=page_id)
        return res.content

    def search(self, query):
        pages = self.search_pages(query)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            try:
                process_list = [executor.submit(self.search_page, page['pageid']) for page in pages['query']['search']]
                docs = [self.post_process(p.result()) for p in process_list]
            except Exception:
                return []
        return docs

    def post_process(self, doc):
        pattern = '|'.join([
            '== References ==',
            '== Further reading ==',
            '== External links',
            '== See also ==',
            '== Sources ==',
            '== Notes ==',
            '== Further references ==',
            '== Footnotes ==',
            '=== Notes ===',
            '=== Sources ===',
            '=== Citations ===',
        ])
        p = re.compile(pattern)
        indices = [m.start() for m in p.finditer(doc)]
        min_idx = min(*indices, len(doc))
        return doc[:min_idx]


class PassageRetrieval:

    def __init__(self, nlp):
        self.tokenize = lambda text: [token.lemma_ for token in nlp(text)]
        self.bm25 = None
        self.passages = None

    def preprocess(self, doc):
        passages = [p for p in doc.split('\n') if p and not p.startswith('=')]
        return passages

    def fit(self, docs):
        passages = list(itertools.chain(*map(self.preprocess, docs)))
        corpus = [self.tokenize(p) for p in passages]
        self.bm25 = BM25(corpus)
        self.passages = passages

    def most_similar(self, question, topn=10):
        tokens = self.tokenize(question)
        average_idf = sum(map(lambda k: float(self.bm25.idf[k]), self.bm25.idf.keys()))
        scores = self.bm25.get_scores(tokens, average_idf)
        pairs = [(s, i) for i, s in enumerate(scores)]
        pairs.sort(reverse=True)
        passages = [self.passages[i] for _, i in pairs[:topn]]
        return passages


class AnswerExtractor:

    def __init__(self, tokenizer, model):
        tokenizer = AutoTokenizer.from_pretrained(tokenizer)
        model = AutoModelForQuestionAnswering.from_pretrained(model)
        self.nlp = QuestionAnsweringPipeline(model=model, tokenizer=tokenizer)

    def extract(self, question, passages):
        answers = []
        for passage in passages:
            try:
                answer = self.nlp(question=question, context=passage)
                answer['text'] = passage
                answers.append(answer)
            except KeyError:
                pass
        answers.sort(key=operator.itemgetter('score'), reverse=True)
        return answers


SPACY_MODEL = os.environ.get('SPACY_MODEL', 'en_core_web_sm')
QA_MODEL = os.environ.get('QA_MODEL', 'distilbert-base-cased-distilled-squad')
translator = Translator()


def translate(text, dest, src='en'):
    try:
        out = translator.translate(text, src=src, dest=dest).text
        return out
    except ValueError:
        return text


def detect_lang(text):
    return translator.detect(text).lang


def translate_ans(answers, dest):
    ans = []
    for answer in answers:
        short_ans = translate(answer['short'], dest)
        long_ans = translate(answer['long'], dest)
        ans.append({"short": short_ans, "long": long_ans})
    return ans


class WikiBot:
    def __init__(self):
        self.nlp = spacy.load(SPACY_MODEL, disable=['ner', 'parser', 'textcat'])
        self.query_processor = QueryProcessor(self.nlp)
        self.document_retriever = DocumentRetrieval()
        self.passage_retriever = PassageRetrieval(self.nlp)
        self.answer_extractor = AnswerExtractor(QA_MODEL, QA_MODEL)

    def answer(self, question):
        query = self.query_processor.generate_query(question)
        docs = self.document_retriever.search(query)
        ans = []
        if len(docs) < 1:
            ans.append({"short": "Out of context", "long": "Unable to find appropriate answer for this question!"})
            return ans
        self.passage_retriever.fit(docs)
        passages = self.passage_retriever.most_similar(question)
        answers = self.answer_extractor.extract(question, passages)
        for answer in answers:
            ans.append({"short": answer["answer"], "long": answer["text"]})
        return ans

    def execute(self, request):
        if request.method == 'POST':
            input_data = request.get_json()
            if input_data:
                if c.input_text in input_data:
                    question = input_data[c.input_text]
                    que_lang = detect_lang(question)
                    out_lang = input_data[c.output_lang]
                    if que_lang != "en":
                        question = translate(question, "en", src=que_lang)
                    answers = self.answer(question)
                    if out_lang == "en":
                        pass
                    elif out_lang == c.output_in_same_lang:
                        if que_lang != "en":
                            answers = translate_ans(answers, que_lang)
                    else:
                        answers = translate_ans(answers, out_lang)
                    output_data = {c.status: c.status_success,
                                   c.title: "Vishwakosh",
                                   c.info: c.info_normal,
                                   c.data: {c.message: answers}}
                    return jsonify(output_data)
                else:
                    output_data = {c.status: c.status_failed,
                                   c.title: "reverse string",
                                   c.info: f"Expecting '{c.input_text}' as input!"}
                    return jsonify(output_data)
            else:
                output_data = {c.status: c.status_failed,
                               c.title: "reverse string",
                               c.info: f"Expecting '{c.input_text}' as input in json format!"}
                return jsonify(output_data)
        else:
            output_data = {c.status: c.status_failed,
                           c.title: "reverse string",
                           c.info: f"Expecting POST method with '{c.input_text}' as input in json format!"}
            return jsonify(output_data)


