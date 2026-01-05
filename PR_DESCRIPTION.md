# Fix circle/ellipse transforms with gradient fills

## Problem
Circles and ellipses with transforms were becoming invisible or completely lost when applying transformations, especially when using gradient fills. This was a critical bug that made the extension unusable for SVG files containing circles/ellipses with gradients.

## Root Causes
1. **Type errors**: Coordinate values (`cx`, `cy`) and radius values (`r`, `rx`, `ry`) were being set as floats instead of strings, causing incorrect SVG output
2. **Invalid circle attributes**: Circles with non-uniform scaling only had `r` attribute set instead of being converted to ellipses with `rx` and `ry`
3. **Missing gradient transformation**: Gradients with `userSpaceOnUse` coordinates were not being transformed along with their shapes, causing them to appear in the wrong location or become invisible

## Solution

### 1. Fixed String Conversion (lines 249-250, 268-269, 271-279)
- Added `str()` conversions for all coordinate and radius values
- Ensures SVG specification compliance

### 2. Circle to Ellipse Conversion (lines 271-279)
- Circles with non-uniform scaling are now properly converted to ellipses
- Old `r` attribute is removed and replaced with correct `rx` and `ry` attributes

### 3. Automatic Gradient Transformation (new methods at lines 171-269)
Added three new methods to handle gradient transformation:

- **`transformGradient(node, transf)`**: Detects gradient references in `fill` attribute or `style` attribute (with correct CSS precedence)
- **`transformRadialGradient(gradient, transf)`**: Transforms radial gradient coordinates:
  - Applies existing `gradientTransform` to get effective position
  - Applies shape's transform to move gradient with the shape
  - Updates cx, cy, fx, fy, and r coordinates
  - Removes `gradientTransform` attribute after applying it
- **`transformLinearGradient(gradient, transf)`**: Transforms linear gradient endpoints (x1, y1, x2, y2)

Gradient transformation is called for both uniform and non-uniform scaling cases (lines ~343 and ~404).

## Testing
- Added test case with circles in groups with transforms and gradient fills
- Verified circles remain visible and gradients are correctly positioned
- Tested with both `fill` attribute and CSS `style` attribute

## Benefits
- Shapes with gradient fills now remain visible after transformation
- Gradients are correctly positioned relative to transformed shapes
- Works with complex nested transforms (groups + individual shapes)
- Handles both radial and linear gradients
- Respects CSS precedence rules (style attribute over fill attribute)

## Compatibility
- Maintains backward compatibility with existing functionality
- Only affects circles, ellipses, and gradients
- No breaking changes to the API or user interface

---

This fix makes the extension usable for a much wider range of SVG files, particularly those created in Inkscape with gradient-filled shapes.
