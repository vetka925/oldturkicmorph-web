from morph import morph_analysis as ma

class Parsing:
    def __init__(self, word):
        self.word = word
        self.parse = ma.morph(self.word)
        self.lemma = [p[0][0] for p in self.parse]
        self.pos = [p[0][1] for p in self.parse]

    def lemmas(self, index):
        lemma = self.lemma
        return lemma[index]

    def poses(self, index):
        pos = self.pos
        return pos[index]

    def affix_chain(self):
        result = []
        for p in self.parse:
            if len(self.parse) > 1:
                result.append(['="'.join(aff)+'"' for aff in p[1:len(p)]])
            else:
                return 0
        return result

    def morph_analysis(self, index):
        affix_chain = []
        lemma = self.lemma
        pos = self.pos
        for p in self.parse:
            affix_chain.append(['="'.join(aff)+'"' for aff in p[1:len(p)]])
        if len(self.parse) > 1:
            return lemma[index]+'="'+pos[index]+'" + '+' + '.join(affix_chain[index])
        else:
            return self.lemma[0]+"="+pos[0]
