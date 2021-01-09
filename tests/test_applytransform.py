# coding=utf-8
from applytransform import ApplyTransform
from inkex.tester import ComparisonMixin, TestCase

class TestApplyTransform(ComparisonMixin, TestCase):
    compare_file = "svg/applytransform.svg"
    effect_class = ApplyTransform
    comparisons = [()]