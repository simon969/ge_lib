Setting up your machine
#########################
To use the ground engineering python function library in your applications or to contribute functions to the library itself you will need to set your machine up 

Install Python
--------------
Got to https://python.org and download the python version you need

Install Git
-----------
Git is a repository that provides collaborative working environment with full version control
WINDOWS
got to https://git-scm.com/download/win
LINUX
.. code-block:: console
    $sudo apt-get install git

Install Microsoft Visual Code Editor
---------------------------------------
Go to https://code.visualstudio.com/download to download Microsoft visual code

Install Pylance Extension
--------------------------
From within code editor add the Pylance extension (CTRL+SHFT+X) (ms-python.vscode-pylance)

Creating and Activating a Virtual Environment
---------------------------------------------
Having installed the pylance extension from the command menu in visual code(CTRL+SHFT+P) 
select "Python:Create Environment"
This will create a .venv folder in your project folder which contains the virtual environment folders. 
The project specific python version and site-packages will be located here.

To activate this environment:

LINUX

.. code-block:: bash

    $ source .venv/bin/activate

WINDOWS

.. code-block:: 

    c:\myproject:>.venv\scripts\activate


The library is maintained in a git repository, following branches are maintained 

Using the function library in your projects you'll need the main (default) branch

main

The main branch is the default branch of the latest QA/QC version for installing in projects (pip install).

.. note::
    As with all evolving work mistakes and errors do occur. While every effort is made to ensure that the library performance correctly, but we cannot always anticipate all the use cases that might occur.
    Please report any unusual behaviour or suspect results particularly give details of the circumstances under which they have occurred so they can be investigated by the development team. 
    It is only with this constant vigilance that we reduce and minimise error for all users. 

To contributing to the function library you'll need the development (dev) branch

dev

The development (dev) branch is for downloading (pull requests). Amendments and additions are then submitted (merge requests).
Periodically the development branch is merged back into the main branch as the next new version
