# coding: utf-8

import sys
from html.parser import HTMLParser
import os
import re
from urllib import request


class Parser(HTMLParser):
    def __init__(self):
        super(Parser, self).__init__()
        self.imgurl = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attr = dict(attrs)
            try:
                self.imgurl.append(attr['src'])
            except KeyError:
                pass


def main():
    parser = Parser()
    target = sys.argv[1]    # target page's URL
    save = sys.argv[2]      # save location
    req = request.urlopen(target)
    # get charset
    c = re.search(r'.*charset=(.+)$', req.getheader('Content-Type'))
    charset = c.group(1) if c is not None else 'utf-8'

    text = req.read().decode(charset)
    parser.feed(text)
    parser.close()

    for c, img in enumerate(parser.imgurl):
        if not img.startswith('http'):
            img = target + img
        request.urlretrieve(img, os.path.join(save, '{:4}'.format(c)))


if __name__ == '__main__':
    main()
