import os
import xml.etree.ElementTree as ET
import dill
from collections import defaultdict, Counter

import re

if __name__ == '__main__':
    categories = {'person_first_nam': 'person', 'person_last_nam': 'person',
                  'country_nam': 'place', 'city_nam': 'place', 'road_nam': 'place'}

    if os.path.isfile('out/potop.index'):
        sentences = dill.load(open('out/potop.sen'))
        index = dill.load(open('out/potop.index'))
    else:
        tree = ET.parse('out/potop.txt.ccl')
        root = tree.getroot()

        sentences = {}
        index = defaultdict(lambda: {'count': Counter(), 'sentences': defaultdict(list)})

        for sentence in root.findall('.//sentence'):
            id = sentence.attrib['id']
            stext = re.sub('\s(?=[,.;\'":?!-()])', '', ' '.join([orth.text for orth in sentence.findall('.//orth')]))
            sentences[id] = stext

            for tok in sentence.findall('tok'):
                orth = tok.find('orth')
                text = orth.text
                base = tok.find('lex/base').text
                ann = tok.findall('ann')
                ann = [a for a in ann if int(a.text) > 0]
                cat = [a.attrib['chan'] for a in ann]

                if len(cat) > 0:
                    index[categories[cat[0]]]['count'][base] += 1
                    index[categories[cat[0]]]['sentences'][base].append(id)

        dill.dump(sentences, open('out/potop.sen', mode='w'))
        dill.dump(dict(index), open('out/potop.index', mode='w'))

    while True:
        name = raw_input('> ').decode('utf-8')
        for cat in index.keys():
            count = index[cat]['count'][name]
            if count > 0:
                print 'Category: {}'.format(cat)
                print 'Occurences: {}'.format(count)
                for s in index[cat]['sentences'][name]:
                    print sentences[s]
                print '\n'
