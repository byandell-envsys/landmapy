# Coding Strategy

- [Coding Strategy](#coding-strategy)
  - [Introduction](#introduction)
  - [Build a Function](#build-a-function)
  - [Add Documentation](#add-documentation)
  - [Put a Function in a File](#put-a-function-in-a-file)
  - [Put reusable Module(s) in their own Directory](#put-reusable-modules-in-their-own-directory)
  - [Build a Package from Modules in a Directory](#build-a-package-from-modules-in-a-directory)
  - [Import Functions from GitHub](#import-functions-from-github)
  - [Add Further Documentation](#add-further-documentation)
    - [Document Functions in Modules in a Package](#document-functions-in-modules-in-a-package)

## Introduction

My approach to coding is organic, intuitive and iterative.
I like to start with a simple, working solution and then build on it.
I find that this approach helps me to better understand the problem
and evolve a simpler, more elegant solution over time.
The goal of my code is to reveal patterns in data
and to make them accessible to others.

[Data evolve](https://byandell.github.io/Data-Evolve/)
over time, and so does code, as my understanding of a project,
and of the patterns in data, grows.
I typically start with something simple.
For instance, when working with envionmental data,
it is often efficient to have a directory (folder) to place data files.
In this course, we started with

```python
import os
import pathlib

data_dir = os.path.join(
    pathlib.Path.home(),
    'earth-analytics',
    'data',
    'habitat'
)
os.makedirs(data_dir, exist_ok=True)
```

## Build a Function

Once I repeatedly use code many times (at least twice),
it is time to create a function that I can reuse.
Note the generalization with a parameter `new_dir`
to allow user to specify a different directory name.

```python
def create_data_dir(new_dir='habitat'):
    import os
    import pathlib

    data_dir = os.path.join(
        pathlib.Path.home(),
        'earth-analytics',
        'data',
        new_dir
    )
    os.makedirs(data_dir, exist_ok=True)

    return data_dir

data_dir = create_data_dir('habitat')
```

## Add Documentation

To remind me of the purpose of the function, I added documentation using
[docstring](https://peps.python.org/pep-0257/).

```python
def create_data_dir(new_dir='habitat'):
    """
    Create Data Directory if it does not exist.

    Args:
        new_dir (char, optional): Name of new directory
    Returns:
        data_dir (char): path to new directory
    """
    import os
    import pathlib

    data_dir = os.path.join(
        pathlib.Path.home(),
        'earth-analytics',
        'data',
        new_dir
    )
    os.makedirs(data_dir, exist_ok=True)

    return data_dir

# data = create_data_dir('habitat')
```

The last comment line is a reminder how to use this function.
Once defined, I follow this suggestion:

```python
data_dir = create_data_dir('habitat')
```

## Put a Function in a File

I then put the function in a (flat) python file,
say using its name `create_data_dir.py`,
which I could import into my notebook or script.

```python
%run create_data_dir.py
```

```python
data_dir = create_data_dir('habitat')
```

The file is re-read from disk with the `%run` magic command,
which is useful for testing the script.
Whenever the file is changed, I need to re-read with `%run`,
with changes to `create_data_dir.py` available immediately.

If the file is in the same folder as my notebook,
I can instead import the function as follows:

```python
from create_data_dir import create_data_dir
data_dir = create_data_dir('habitat')
```

However, to use `import` most effectively requires a few more steps.

## Put reusable Module(s) in their own Directory

The
[references](references.md)
become useful at this point,
particularly
[IPython Interactive Computing](https://ipython.org/ipython-doc/3/interactive/tutorial.html).
When using `import`,
we specifically reload the "module",
as we do with many of the python packages.
Basically a `*.py` file is a module,
and a directory containing `*.py` files is the beginnings of a package
containing multiple modules.
This is academic at this point, but becomes important when working
with larger and/or multiple projects.

Since I plan to use this function in multiple projects,
I will separate it from any particular project by putting it in its own place.
For my purposes, I have projects in folder `~/Documents/GitHub/`,
so I will put the function in a folder `~/Documents/GitHub/landmapy/`.
For technical reasons (below), I put the function in a subfolder,
also called `landmapy`.
Further, I expect to have several initializing functions,
so I placed `create_data_director()` in a file
[initial.py](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/initial.py).

On my local machine, I have the code for function `create_data_directory()`
in module (file)
`~/Documents/GitHub/landmapy/landmapy/initial.py`.
I `%run` the function in this file

```python
%run ~/Documents/GitHub/landmapy/landmapy/initial.py
```

and use it as before,

```python
data_dir = create_data_dir('habitat')
```

## Build a Package from Modules in a Directory

Now I have a separate place for code functions used repeatedly,
possibly across multiple projects.
Over time, I create more functions and store them in files in this same place,
`~/Documents/GitHub/landmapy/landmapy/`.
While I can `%run` each file as needed as shown above,
it is more efficient to create a package,
which is a directory containing multiple modules.

I chose to call my repo
[landmapy](https://github.com/byandell-envsys/landmapy)
because it has python functions for land cover mapping.
(I earlier created a repo called
[landmapr](https://github.com/byandell-envsys/landmapr)
with R code for land cover mapping.)

Again, the
[references](references.md)
become useful at this point, particularly
[Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/).
This shows steps beyond organizing modules in a directory,
to creating a package that can be installed and imported into any project.
We start with the following directory structure:

```
landmapy/
    landmapy/
        __init__.py
        initial.py
```

The `__init__.py` is a special file,
which can be empty,
required by python to identify this directory is a package.

```
landmapy/
    LICENSE         # code license (typically open source)
    README.md       # overview of the package
    pyproject.toml  # or setup.py (there seem to be two ways to do this)
    landmapy/       # package directory (this is the name the package will be imported as)
        __init__.py # tells python this is a package
        initial.py  # module containing functions
```

I can now import functions from the package as needed after I install the package with 
[pip](https://pypi.org/project/pip/):

```python
#| eval: False
pip install ~/Documents/GitHub/landmapy
```

The import is slightly different as we access the `initial` module from the `landmapy` package
and import the function `create_data_dir` from that module.
(The comment line `#| eval: False` is a directive to the markdown interpreter
to not evaluate the following code block.)

```python
from landmapy.initial import create_data_dir
data_dir = create_data_dir('habitat')
```

## Import Functions from GitHub

Building a package adds more machinery,
but it enables me to import a variety of functions
that I maintain on GitHub in a single location, the package
[landmapy](https://github.com/byandell-envsys/landmapy).
This package is a repo, just like repos for other projects.

From GitHub, I (and anyone else) can install the package with 
[pip](https://pypi.org/project/pip/):

```python
#| eval: False
pip install git+https://github.com/byandell-envsys/landmapy.git
```

(Again, comment line `#| eval: False` suppresses markdown evaluation.)
As before, I can import the function as follows:


```python
from landmapy.initial import create_data_dir
data_dir = create_data_dir('habitat')
```

## Add Further Documentation

Documentation evolves, just as do data, code, and each data-rich project.
My future self, and other users of my code, benefit from documentation
of how functions work, why they are organized in modules,
and what might still be needed to improve a package or project.
The
[References](references.md)
draw on documentation created by the broader community.
This
[Coding Strategy](strategy.md)
page is another form of documentation.
In addition, each project that uses the package can have
its own (compact) documentation referring to the
[landmapy](https://github.com/byandell-envsys/landmapy)
and explaining how and why package tools are employed.

### Document Functions in Modules in a Package

Of course, I can add more functions to the package,
but I am mindful that as the package grows,
the need for coherent documentation expands.
I add one-line function calls in
[landmapy/\_\_init\_\_.py](landmapy/__init__.py)
and adapt the 
[README.md](README.md)
to describe how to access and use the package,
provide use cases,
and organize modules and functions by topic.
There is a balance of adding documentation and keeping it simple.
My documentation process has evolved to the following approach:

- Add a docstring to each function in a module `*.py`
- Add one-line function descriptions in the top docstring of the module `*.py`
- Add one-line function calls in the `landmapy/__init__.py` file
- Add one-line module and function information in the `README.md` file

The `landmapy` package is now large enough that I find it helpful to organize
[Package Modules and Functions](README.md#package-modules-and-functions)
in the
[README.md](README.md)
into (drop-down) blocks around topics:

- Plot Data
- Access Data with APIs
- Explore Data
- Set up Data Mechanics

Readers can then expand the block for a particular module to see the functions contained therein.