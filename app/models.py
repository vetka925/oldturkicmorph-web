from app import db

class Lemmas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lemma = db.Column(db.String())
    pos = db.Column(db.String())
    bashkir_translate = db.Column(db.String())
    russian_translate = db.Column(db.String())
    english_translate = db.Column(db.String())
    etimology = db.Column(db.String())

    def __init__(self, lemma, pos, bashkir_translate='None', russian_translate='None', etimology='None'):
        self.lemma = lemma
        self.pos = pos
        self.bashkir_translate = bashkir_translate
        self.russian_translate = russian_translate
        self.etimology = etimology

    def __repr__(self):
        return '<Lemma %r>' % (self.lemma)

class Parsings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order = db.Column(db.Integer)
    word = db.Column(db.String())
    lemma = db.Column(db.String())
    pos = db.Column(db.String())
    affix_chain = db.Column(db.String())

    def __init__(self, word, lemma, pos, affix_chain):
        self.word = word
        self.lemma = lemma
        self.pos = pos
        self.affix_chain = affix_chain

    def __repr__(self):
        return '<Pars %r>' % (self.word)

class Graph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String())
    graph = db.Column(db.PickleType)

    def __init__(self, lang, graph):
        self.lang = lang
        self.graph = graph

class Interpretation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String())
    ru = db.Column(db.String())
    en = db.Column(db.String())
    bash = db.Column(db.String())

    def __init__(self, tag, ru, en, bash):
        self.tag = tag
        self.ru = ru
        self.en = en
        self.bash = bash
