#!/usr/bin/env python3
import sys
sys.path.insert(0, '.')

from applytransform import ApplyTransform

# Run on the simple test file
effect = ApplyTransform()
effect.run(['tests/data/svg/circle_in_group_with_transform.svg'])
