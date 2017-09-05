# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 12:37:51 2017

@author: vital
"""
import pickle
import networkx as nx
import codecs
import re
from morph import dictionaries as dic
from morph import lemmas_dict as lem
from config import basedir
from app import models, db

if modlels.Graph.query.filter_by(language='oldturkic').first() != None:
    G = pickle.loads(modlels.Graph.query.filter_by(language='oldturkic').first().graph)

def get_lem(word):
    result = {}
    lemmas_dict = lem.lemmas_dict
    if word in lemmas_dict:
        result[word] = lemmas_dict[word]
    else:
        for l in models.Lemmas.query.all():
            if l.lemma == word[:len(l.lemma)]:
                if l.pos not in dic.non_inflected:
                    result[l.lemma] = l.pos
    return result

def last_possible_aff(word):
    result = []
    for n in G.nodes():
        for (aff, tag) in G.node[n]:
            if aff == word[-len(aff):]:
                result.append([((aff, tag), word[:-len(aff)])])
    return result

def get_next_aff(affix, chain):
    result = []
    for node in G.nodes():
        if affix in G.node[node]:
            for next_node in G.successors(node):
                for next_aff in G.node[next_node]:
                    if next_aff[0] == chain[-len(next_aff[0]):]:
                        next_chain = chain[:-len(next_aff[0])]
                        result.append((next_aff, next_chain))
    return result

def one_step(lst):
    last_aff = lst[len(lst)-1]
    next_aff = get_next_aff(last_aff[0], last_aff[1])
    result = []
    for aff in next_aff:
        next_lst = lst.copy()
        next_lst.append(aff)
        result.append(next_lst)
    return result

def check_for_lemma(list_of_possible_pars):
    lst = list_of_possible_pars
    if lst[len(lst)-1][1] in lemmas_dict:
        return lst


def check_list_for_pars(lst):
    count = []
    for l in lst:
        step = one_step(l)
        if step == []:
            z=False
            count.append(z)
        else:
            z=True
            count.append(z)
    if True in count: return True
    else: return False

def predict_pos(first_aff):
    result = []
    for node in G.nodes():
        if first_aff in G.node[node]:
            for p in dic.pos:
                if p in G.successors(node):
                    result.append(p)

    res = '/'.join(result)
    return res

def reverse_pars(pars, word):
    result = []
    possible_lemmas = get_lem(word)
    lemma_aff = pars.pop()
    first_aff = lemma_aff[0]
    if lemma_aff[1] in possible_lemmas:
        lemma = (lemma_aff[1], possible_lemmas[lemma_aff[1]])
    else:
        lemma = (lemma_aff[1], predict_pos(first_aff))
    for morph in pars:
        result.append(morph[0])
    result.append(first_aff)
    result.append(lemma)
    result.reverse()
    return result

def parsing(word):
    start = last_possible_aff(word)
    while check_list_for_pars(start) == True:
        result = []
        for lst in start:
            if len(one_step(lst)) == 0:
                result.append(lst)
                continue
            else:
                result.extend(one_step(lst))
        start = result
    return start

def morph(w):
    possible_lemmas = get_lem(w)
    result = []
    if possible_lemmas != {}:
        if w in possible_lemmas:
            return [(w, possible_lemmas[w])]
        else:
            for l in possible_lemmas:
                chain = w[len(l):]
                possible_parses = parsing(chain)
                parses = [pars for pars in possible_parses if pars[len(pars)-1][1] == '']
                for p in parses:
                    tmp = []
                    for morph in p:
                        tmp.append(morph[0])
                    tmp.append((l, possible_lemmas[l]))
                    tmp.reverse()
                    result.append(tmp)
    if result == []:
        print(w)
        possible_parses = parsing(w)
        for pars in possible_parses:
            tmp = []
            lemma_aff = pars.pop()
            first_aff = lemma_aff[0]
            lemma = (lemma_aff[1], predict_pos(first_aff))
            if pars == []:
                tmp.append(lemma)
                tmp.append(first_aff)
                result.append(tmp)
            else:
                print('yes')
                for morph in pars:
                    tmp.append(morph[0])
                tmp.append(first_aff)
                tmp.append(lemma)
                result.append(tmp)
                result.reverse()

    return result
