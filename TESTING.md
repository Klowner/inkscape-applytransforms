# Tests

This Inkscape extension is tested with comparison tests.

## Running Tests

You must install the program `pytest` in order to run these tests. Both Pytest and Pytest-Coverage are required to run tests.

Usually the best way to install it is: 

```shell
$ pip3 install -r tests/dev_requirements.txt
```

You may run all tests by omitting any other parameters.

```shell
$ pytest
```

## Test Files

The test files are in the `tests` directory. This test is a "comparison" test. It will fail whenever the output changes, so it will need to be updated to reflect changes.


## Test Data

As well as python test files, each test will normally depend on additional data. From source svg files, to output comparison tests and other such things.

This data is always held in `tests/data`. Source svg files go in to `tests/data/svg`, output comparison files in to `tests/data/refs`.
When writing tests, please make sure your data goes into the right directory. If you are updating the comparison test,
usually you just need to rename the `export` file generated and remove the `.export` suffix to enable it.

To do so run the following command:

```shell
EXPORT_COMPARE=1 $ pytest
```

This will write a new output comparison file in to `tests/data/refs`.


## Testing Options

Tests can be run with these options that are provided as environment variables:

    FAIL_ON_DEPRECATION=1 - Will instantly fail any use of deprecated APIs
    EXPORT_COMPARE=1 - Generate output files from comparisons. This is useful for manually checking the output as well as updating the comparison data.
    NO_MOCK_COMMANDS=1 - Instead of using the mock data, actually call commands. This will also generate the msg files similar to export compare.
    INKSCAPE_COMMAND=/other/inkscape - Use a different Inkscape (for example development version) while running commands. Works outside of tests too.
    XML_DIFF=1 - Attempt to output an XML diff file, this can be useful for debugging to see differences in context.
    DEBUG_KEY=1 - Export mock file keys for debugging. This is a highly specialised option for debugging key generation.


## More Information

For further details see the official Inkscape Extension repository, currently residing at: https://gitlab.com/inkscape/extensions/-/blob/master/TESTING.md