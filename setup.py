from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='AECOM UK Ground Engineering Function Library',
    url='https://github.com/simon969/ge_lib',
    author='Simon Thomson',
    author_email='simon.thomson@aecom.com',
    # Needed to actually package something
    # packages=['found'],
    package_dir={'': 'src'},
    # py_modules = ["module_1", "module_2"],
    # Needed for dependencies
    install_requires=[
                    'importlib-metadata==4.8.2',
                    'packaging==23.2',
                    'pypyodbc==1.3.6',
                    'pandas>=1.5.3',
                    'numpy>=1.26.4',
                    'numpy-utils>=0.1.6',
                    'python-AGS4>=0.5.0',
                    'tomli==2.0.1',
                    'zipp==3.6.0',
                    'ipykernel>=6.29.0',
                    'dict2xml==1.7.4',
                    'unixodbc-dev',
                    'pycryptodome>=3.20.0',
                    'chardet>5.2.0',
                    'matplotlib>=3.8.2',
                    'qtconsole>=5.5.1',
                    'urllib3>=2.2.0'
                    ],
    # unixodbc is needed for pypyodbc on linux system  (https://github.com/mkleehammer/pyodbc/issues/36)
    
    # *strongly* suggested for sharing
    version='0.0.1',
    # The license can be anything you like
    license='MIT',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)