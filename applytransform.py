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
import math
import simplestyle
from simpletransform import composeTransform, fuseTransform, parseTransform, applyTransformToPath, applyTransformToPoint, formatTransform

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

    def recursiveFuseTransform(self, node, transf=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]):
        transf = composeTransform(transf, parseTransform(node.get("transform", None)))

        if 'transform' in node.attrib:
            del node.attrib['transform']

        if 'style' in node.attrib:
            style = node.attrib.get('style')
            style = simplestyle.parseStyle(style)
            update = False

            if 'stroke-width' in style:
                try:
                    stroke_width = self.unittouu(style.get('stroke-width').strip())
                    # pixelsnap ext assumes scaling is similar in x and y
                    # and uses the x scale...
                    # let's try to be a bit smarter
                    # the least terrible option is using the geometric mean
                    stroke_width *= math.sqrt(transf[0][0] * transf[1][1])
                    style['stroke-width'] = str(stroke_width)
                    update = True
                except AttributeError:
                    pass

            if update:
                style = simplestyle.formatStyle(style)
                node.attrib['style'] = style

        node = ApplyTransform.objectToPath(node)

        if 'd' in node.attrib:
            d = node.get('d')
            p = cubicsuperpath.parsePath(d)
            applyTransformToPath(transf, p)
            node.set('d', cubicsuperpath.formatPath(p))

        elif node.tag in [inkex.addNS('polygon', 'svg'),
                          inkex.addNS('polyline', 'svg')]:
            points = node.get('points')
            points = points.strip().split(' ')
            for k,p in enumerate(points):
                if ',' in p:
                    p = p.split(',')
                    p = [float(p[0]),float(p[1])]
                    applyTransformToPoint(transf, p)
                    p = [str(p[0]),str(p[1])]
                    p = ','.join(p)
                    points[k] = p
            points = ' '.join(points)
            node.set('points', points)

        elif node.tag in [inkex.addNS('rect', 'svg'),
                          inkex.addNS('text', 'svg'),
                          inkex.addNS('image', 'svg'),
                          inkex.addNS('use', 'svg'),
                          inkex.addNS('circle', 'svg')]:
            node.set('transform', formatTransform(transf))

        for child in node.getchildren():
            self.recursiveFuseTransform(child, transf)


if __name__ == '__main__':
    e = ApplyTransform()
    e.affect()
