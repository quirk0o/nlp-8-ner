import xml.etree.ElementTree as ET

from collections import defaultdict, Counter

import re

from dill import dill

if __name__ == '__main__':
    categories = {'person_first_nam': 'person', 'person_last_nam': 'person', 'country_nam': 'place',
                  'city_nam': 'place', 'road_nam': 'place'}

    sentences = dill.load(open('out/potop.sen'))
    index = dill.load(open('out/potop.index'))

    for cat in index.keys():
        print 'Most common in category: {}'.format(cat)
        for token, occurences in Counter(index[cat]['count']).most_common(10):
            print token
            print 'Occurences: {}'.format(occurences)

        print '----------------------------------------'
