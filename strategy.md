# Coding Strategy

My approach to coding is organic, intuitive and iterative.
I like to start with a simple, working solution and then build on it.
I find that this approach helps me to better understand the problem
and evolve a simpler, more elegant solution over time.
The goal of my code is to reveal patterns in data
and to make them accessible to others.

[Data evolve](https://byandell.github.io/Data-Evolve/)
over time, and so does code as my understanding of the project,
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

## Building a Function

Once I realized I would reuse this many times (at least twice),
I created a function to do this for me.
Not the generalization with `new_dir` to allow for different directory names.

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
```

## Adding Documentation

To remind me of the purpose of the function, I added a documentation using
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

# create_data_dir('habitat')
```

## Putting the Function in a File

I then put it in a (flat) python file,
say using its name `create_data_dir.py`,
which I could import into my notebook or script.

```python
%run create_data_dir.py
```

The file is re-read from disk each time when using the `%run` magic command,
which is useful for testing the script,
and changes you make to `create_data_dir.py` are reflected immediately.

It is also possible to import the function as follows:

```python
from create_data_dir import create_data_dir
```

## Modules and Packages

The
[references](references.md)
become useful at this point,
particularly
[IPython Interactive Computing](https://ipython.org/ipython-doc/3/interactive/tutorial.html).
When using `import`,
we are specifically reloaded the "module",
as we do with many of the python packages.
Basically a `*.py` file is a module,
and a directory containing `*.py` files is a package.
This is academic at this point, but becomes important when working
with larger and/or multiple projects.

Since I plan to use this function in multiple projects,
I will separate it from any particular project by putting it in a new GitHub repo.
I chose to call my repo
[landmapy](https://github.com/byandell-envsys/landmapy)
because I plan populate it with python functions for land cover mapping.
(I earlier created a repo called
[landmapr](https://github.com/byandell-envsys/landmapr)
with R code for land cover mapping.)

Further, I expect to have several initializing functions,
so I placed them in a file
[initial.py](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/initial.py).
On my local machine, I have the code in
`~/Documents/GitHub/landmapy/landmapy/initial.py`,
so I could import the function as follows:

```python
%run ~/Documents/GitHub/landmapy/landmapy/initial.py
```

It is possible to `import` the function from a file in a different directory,
but it is complicated and not probably recommended.
Rather, it is useful to build a package, as I have done with `landmapy`.
This adds more machinery, but it enables me to import a variety of functions
that I maintain on GitHub in a single location, the package
[landmapy](https://github.com/byandell-envsys/landmapy).

I can use this package in a project by installing it from my local directory with 
[pip](https://pypi.org/project/pip/):

```python
pip install ~/Documents/GitHub/landmapy
```

Or I (and anyone else) can install it from GitHub with:

```python
#| eval: False
pip install git+https://github.com/byandell-envsys/landmapy.git
```

This is done only once, or whenever the package is updated.
I can now import the function as follows:


```python
from landmapy.initial import create_data_dir
```
