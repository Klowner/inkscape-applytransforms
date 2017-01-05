#!/usr/bin/env python2
#
# License: GPL2
# Copyright Mark "Klowner" Riedesel
# https://github.com/Klowner/inkscape-applytransforms
#
import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex
import cubicsuperpath
from simpletransform import composeTransform, fuseTransform, parseTransform, applyTransformToPath, formatTransform

class ApplyTransform(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        self.getselected()

        if self.selected:
            for id, shape in self.selected.items():
                self.recursiveFuseTransform(shape, parseTransform(None))
        else:
            self.recursiveFuseTransform(self.document.getroot(), parseTransform(None))

    @staticmethod
    def objectToPath(node):
        if node.tag == inkex.addNS('g', 'svg'):
            return node

        if node.tag == inkex.addNS('path', 'svg') or node.tag == 'path':
            for attName in node.attrib.keys():
                if ("sodipodi" in attName) or ("inkscape" in attName):
                    del node.attrib[attName]
            return node

        return node

    @staticmethod
    def recursiveFuseTransform(node, transf=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]):
        transf = composeTransform(transf, parseTransform(node.get("transform", None)))

        if 'transform' in node.attrib:
            del node.attrib['transform']

        node = ApplyTransform.objectToPath(node)

        if 'd' in node.attrib:
            d = node.get('d')
            p = cubicsuperpath.parsePath(d)
            applyTransformToPath(transf, p)
            node.set('d', cubicsuperpath.formatPath(p))

        elif node.tag == inkex.addNS('rect', 'svg'):
            node.set('transform', formatTransform(transf))

        for child in node.getchildren():
            ApplyTransform.recursiveFuseTransform(child, transf)


if __name__ == '__main__':
    e = ApplyTransform()
    e.affect()
