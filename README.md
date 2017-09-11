# inkscape-applytransforms
An Inkscape extension which recursively applies transformations to shapes.

Note that performing this operation on certain shapes (stars, lpes, ...) will convert them to paths,
and clones are affected in strange ways due to clone transforms behave.

**update 2016-1-5** - now only affects selected shapes when there is an active selection.

## Installation

Download `applytransform.inx` and `applytransform.py`, then copy them to the Inkscape installation folder subdirectory `share\extensions`. On Windows this may be `C:\Program Files\Inkscape\share\extensions`. If the downloaded files have `.txt` suffixes added by GitHub, be sure to remove them. Restart Inkscape if it's running.

## Usage

Activate the extension from the main menu:

> Extensions | Modify Path | Apply Transform
