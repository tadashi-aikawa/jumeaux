# -*- coding:utf-8 -*-


import html.parser


class HTMLToDictParser(html.parser.HTMLParser):
    """
    Original is http://www.xavierdupre.fr/blog/2013-10-27_nojs.html
    """
    def __init__(self, raise_exception=True):
        html.parser.HTMLParser.__init__(self)
        self.doc = {}
        self.path = []
        self.cur = self.doc
        self.line = 0
        self.raise_exception = raise_exception

    @staticmethod
    def do(content, raise_exception=True):
        parser = HTMLToDictParser(raise_exception=raise_exception)
        parser.feed(content)
        return parser.doc

    def handle_starttag(self, tag, attrs):
        self.path.append(tag)
        attrs = {k: v for k, v in attrs}
        if tag in self.cur:
            if isinstance(self.cur[tag], list):
                self.cur[tag].append({"__parent__": self.cur})
                self.cur = self.cur[tag][-1]
            else:
                self.cur[tag] = [self.cur[tag]]
                self.cur[tag].append({"__parent__": self.cur})
                self.cur = self.cur[tag][-1]
        else:
            self.cur[tag] = {"__parent__": self.cur}
            self.cur = self.cur[tag]

        for a, v in attrs.items():
            self.cur["#" + a] = v
        self.cur["##value"] = ""

    def handle_endtag(self, tag):
        if tag != self.path[-1] and self.raise_exception:
            message = "html is malformed around line: {0} (it might be because of a tag <br>, <hr>, <img .. > not closed)"
            raise Exception(message.format(self.line))
        del self.path[-1]
        memo = self.cur
        self.cur = self.cur["__parent__"]
        self.clean(memo)

    def handle_data(self, data):
        self.line += data.count("\n")
        if "##value" in self.cur:
            self.cur["##value"] += data

    def clean(self, values):
        keys = list(values.keys())
        for k in keys:
            v = values[k]
            if isinstance(v, str):
                c = v.strip(" \n\r\t")
                if c != v:
                    if len(c) > 0:
                        values[k] = c
                    else:
                        del values[k]
        del values["__parent__"]

