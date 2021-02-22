# coding=utf-8

import os
from glob import glob

from applytransform import ApplyTransform
from inkex.tester import ComparisonMixin, TestCase
from inkex.tester.inx import InxMixin


class TestApplyTransform(ComparisonMixin, TestCase):
    compare_file = "svg/applytransform.svg"
    effect_class = ApplyTransform
    comparisons = [()]


class TestApplyTransformInx(InxMixin, TestCase):
    def test_inx_file(self):
        for inx_file in glob(os.path.join(self._testdir(), '..', '*.inx')):
            self.assertInxIsGood(inx_file)
