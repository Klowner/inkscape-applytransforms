# inkscape-applytransforms
An Inkscape extension which recursively applies transformations to shapes.

Note that performing this operation on certain shapes (stars, lpes, ...) will convert them to paths,
and clones are affected in strange ways due to clone transforms behave.

**update 2020-7-27** - updated to work with Inkscape 1.0+. Use legacy branch `inkscape-pre1.0-compat` for prior version of Inkscape.

**update 2016-1-5** - now only affects selected shapes when there is an active selection.

## Installation

Download `applytransform.inx` and `applytransform.py`, then copy them to the Inkscape installation folder subdirectory `share\inkscape\extensions`.
  * On Windows this may be `C:\Program Files\Inkscape\share\inkscape\extensions` (or `%appdata%\inkscape\extensions` if you don't want to install globally)
  * On Ubuntu, this may be `/usr/share/inkscape/extensions/` or (`~/.config/inkscape/extensions` if you don't want to install globally)
  * On macOS, this may be (the hidden folder) `~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions`
  * Generally, you should be able to go to the Inkscape Preferences, select `System`, and see the path for `User extensions`
  
If the downloaded files have `.txt` suffixes added by GitHub, be sure to remove them. Restart Inkscape if it's running.

### Arch Linux
This package is also available via the [AUR](https://aur.archlinux.org/packages/inkscape-applytransforms-git/).
```bash
pacaur -S inkscape-applytransforms-git
```

## Usage

Activate the extension from the main menu:

> Extensions | Modify Path | Apply Transform

or use it from the command line. The id of the extension is automatically available as an action:

> `inkscape -g --actions com.klowner.filter.apply-transform test.svg`

or for older versions of Inkscape:

> `inkscape -g --verb com.klowner.filter.apply_transform test.svg`

## Changes

This version includes a number of improvements and bug fixes from the original repository, including:

*   **Text and Tspan Transformation:** Now correctly applies transformations to `text` and `tspan` elements, including scaling of font size.
*   **Rectangle Scaling Fix:** Corrected the scaling logic for rectangles.
*   **Stroke Width Scaling Fix:** Improved stroke width scaling to handle both `style` and direct attributes.
*   **ValueError Fix:** Made the `scaleMultiple` function more robust to prevent a `ValueError`.
*   **Improved Circle and Ellipse Handling with Gradient Support (NEW):**
    *   Simple transformations (translation and uniform scaling) are now applied to circles and ellipses without issuing a warning. Warnings are only shown for complex transformations that might distort the shape.
    *   **Fixed critical bug** where circles and ellipses with transforms were becoming invisible or lost due to incorrect attribute type handling. All coordinate values (`cx`, `cy`) and radius values (`r`, `rx`, `ry`) are now properly converted to strings as required by the SVG specification.
    *   Circles with non-uniform scaling are now correctly converted to ellipses with proper `rx` and `ry` attributes instead of failing with invalid `r` values.
    *   **Automatic Gradient Transformation (NEW):** Radial and linear gradients with `userSpaceOnUse` coordinates are now automatically transformed along with their shapes:
        *   Gradient coordinates (cx, cy, fx, fy, r for radial; x1, y1, x2, y2 for linear) are transformed to follow the shape
        *   Existing `gradientTransform` attributes are properly applied and incorporated
        *   CSS `style` attribute takes precedence over `fill` attribute when detecting gradient references
        *   Shapes with gradient fills now remain visible and correctly rendered after transformation
*   **clipPath and linearGradient Handling:** Added basic handling for `clipPath` and `linearGradient` elements. The extension will now apply the transform to the element and issue a warning.
*   **Testing:** The extension is now tested, and all tests are passing.
