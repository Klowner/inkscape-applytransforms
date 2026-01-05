# coding=utf-8

import os
from glob import glob
from io import BytesIO

from inkex.tester import ComparisonMixin, TestCase
from inkex.tester.inx import InxMixin
from inkex.tester.mock import Capture

from applytransform import ApplyTransform


class TestApplyTransform(ComparisonMixin, TestCase):
    compare_file = "svg/applytransform.svg"
    effect_class = ApplyTransform
    comparisons = [()]


class TestApplyTransformCubes(ComparisonMixin, TestCase):
    compare_file = "svg/cubes.svg"
    effect_class = ApplyTransform
    comparisons = [()]

    def get_compare_cmpfile(self, args, addout=None):
        return self.data_file("refs", "cubes.out")

    def assertEffect(self, *filename, **kwargs):
        if filename:
            data_file = self.data_file(*filename)
        else:
            data_file = self.empty_svg

        os.environ["DOCUMENT_PATH"] = data_file
        args = [data_file] + list(kwargs.pop("args", []))
        args += [f"--{kw[0]}={kw[1]}" for kw in kwargs.items()]

        effect = kwargs.pop("effect", self.effect_class)()

        if self.stderr_output:
            with Capture("stderr") as stderr:
                effect.run(args, output=BytesIO())
                effect.test_output = stderr
        else:
            output = BytesIO()
            with Capture(
                "stdout", kwargs.get("stdout_protect", self.stdout_protect)
            ) as stdout:
                with Capture(
                    "stderr", kwargs.get("stderr_protect", self.stderr_protect)
                ) as stderr:
                    effect.run(args, output=output)
            effect.test_output = output

        if os.environ.get("FAIL_ON_DEPRECATION", False):
            warnings = getattr(effect, "warned_about", set())
            effect.warned_about = set()  # reset for next test
            self.assertFalse(warnings, "Deprecated API is still being used!")

        return effect


class TestApplyTransformInx(InxMixin, TestCase):
    def test_inx_file(self):
        for inx_file in glob(os.path.join(self._testdir(), "..", "*.inx")):
            self.assertInxIsGood(inx_file)
