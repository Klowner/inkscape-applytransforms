#!/usr/bin/env python2
#
# License: GPL2
# Copyright Mark "Klowner" Riedesel
# https://github.com/Klowner/inkscape-applytransforms
#
import sys
sys.path.append('/usr/share/inkscape/extensions')

import inkex, math
from inkex.paths import CubicSuperPath, Path
from inkex.transforms import Transform
from inkex.styles import Style

class ApplyTransform(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    def effect(self):
        self.svg.get_selected()

        if self.svg.selected:
            for id, shape in self.svg.selected.items():
                self.recursiveFuseTransform(shape)
        else:
            self.recursiveFuseTransform(self.document.getroot())

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

    def scaleStrokeWidth(self, node, transf):
        if 'style' in node.attrib:
            style = node.attrib.get('style')
            style = dict(Style.parse_str(style))
            update = False

            if 'stroke-width' in style:
                try:
                    stroke_width = float(style.get('stroke-width').strip())
                    stroke_width *= math.sqrt(abs(transf.a * transf.d))
                    style['stroke-width'] = str(stroke_width)
                    update = True
                except AttributeError:
                    pass

            if update:
                node.attrib['style'] = Style(style).to_str()

    def recursiveFuseTransform(self, node, transf=[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]):
        transf = Transform(transf) * Transform(node.get("transform", None))

        if 'transform' in node.attrib:
            del node.attrib['transform']

        node = ApplyTransform.objectToPath(node)

        if 'd' in node.attrib:
            d = node.get('d')
            p = CubicSuperPath(d)
            p = Path(p).to_absolute().transform(transf, True)
            node.set('d', Path(CubicSuperPath(p).to_path()))

            self.scaleStrokeWidth(node, transf)

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

            self.scaleStrokeWidth(node, transf)

        elif node.tag in [inkex.addNS('rect', 'svg'),
                          inkex.addNS('text', 'svg'),
                          inkex.addNS('image', 'svg'),
                          inkex.addNS('use', 'svg'),
                          inkex.addNS('circle', 'svg')]:
            # node.set('transform', str(Transform(transf)))
            inkex.utils.errormsg("Shape %s not yet supported" % node.tag)

        else:
            # e.g. <g style="...">
            self.scaleStrokeWidth(node, transf)

        for child in node.getchildren():
            self.recursiveFuseTransform(child, transf)


if __name__ == '__main__':
    e = ApplyTransform()
    e.run()
