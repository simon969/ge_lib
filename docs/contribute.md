# Contributing to ge_lib

For full documentation visit [mkdocs.org](https://www.mkdocs.org).
## Project layout

    mkdocs.yml      # The mkdocs build configuration file.
    pyproject.toml  # The build setup file 
    setup.cfg       # the setup config file
    docs/
        index.md    # The documentation homepage.
        AGS.md
        found.md
        motions.md
        plaxis.md
        general.md
        ...         # Other markdown pages, images and other files.
    src/ge_lib/      
        ags          
        found
        general
        motions
        plaxis
        tunnel
        ...         # Other function library modules
    src/tests/
        test_ags/
            data
        test_found/
            data
        test_motions/
            data
        test_plaxis/
            data
        ...        # Other function tests modules
## Check existing modules Create a module

Check the `src\ge_lib\` folder for existing modules and create a folder to save your modules in
If you are contributing to an existing module than you can just save any additional files and folders there.  

## Create a documentation files

Install local markup libraries

* `pip install mkdocs` - Install MkDocs 
* `pip install mkdocstrings` - Install plugin for mkdocs [mkdocstrings](https://mkdocstrings.github.io/python/)
* `pip install mkdocstrings-python` - Install python handler for mkdocstrings [mkdocstrings-python](https://pypi.org/project/mkdocstrings-python/#description)
* `pip install mkdocs-gen-files` - Installs plugin for mkdocstrings [mkdocs-gen-files](https://oprypin.github.io/mkdocs-gen-files/)

Add a documentation markup file (*.md) in the docs directory
The comments in your code will automatically generate markup files, see [mkdocstrings/recipes](https://mkdocstrings.github.io/recipes/). You should also include additional documentation for use cases for functions 

Run the  MkDocs server to view your documentation files along with all others

* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.


## Create unit_tests 

Create unit tests in a new folder in `src\tests` that confirm that your functions are producing the correct results. Test input data and output results for your module should be saved in `src\tests\[my_module]\data` folder

These tests are run across the whole library and a report is produced to confirm that it complies with QA/QC.  
