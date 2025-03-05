# Python References

This is a collection of Python references that I have found useful.
See related in
[EDA References](https://github.com/byandell-envsys/EarthDataAnalytics/blob/main/references.md)
Please offer suggestions to improve.


## Python Coding

- [Python Tutorial](https://docs.python.org/3/tutorial/)
  - [Modules](https://docs.python.org/3/tutorial/modules.html)
- [Pandas Library](https://pandas.pydata.org/docs/)
  - [Pandas Tutorial](https://pandas.pydata.org/docs/user_guide/10min.html)
  - [Pandas API Reference](https://pandas.pydata.org/docs/reference/)
- [EDA Scientific Data Structures in Python](https://www.earthdatascience.org/courses/intro-to-earth-data-science/scientific-data-structures-python/)
  -  [EDA 4. Set Up Your Conda Earth Analytics Python Environment Setup earth analytics environment](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-python-conda-earth-analytics-environment/)
      - [Python venv: How To Create, Activate, Deactivate, And Delete](https://python.land/virtual-environments/virtualenv) 
  - [EDA 6.15. Intro to Pandas Dataframes](https://www.earthdatascience.org/courses/intro-to-earth-data-science/scientific-data-structures-python/pandas-dataframes/)
  - [Subtract One Raster from Another and Export a New GeoTIFF in Open Source Python](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/raster-data-processing/subtract-rasters-in-python/)
  - [Earth Analytics Python Env](https://github.com/earthlab/earth-analytics-python-env)
- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Try and Except code for NetCDF](https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/get-maca-2-climate-data-netcdf-python/);
- [Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code/)
  - [Hitchhikers Guide to Documentation](https://docs.python-guide.org/writing/documentation/)
    - [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/#introduction)
    - [PEP 257: Docstring Conventions](https://peps.python.org/pep-0257/)
  - [Documentation in Python: Methods and Best Practices](https://swimm.io/learn/code-documentation/documentation-in-python-methods-and-best-practices)
- [Python Developer’s Guide](https://devguide.python.org/)
- [Integrating Python Code With R](https://www.geeksforgeeks.org/integrating-python-code-with-r/)

### IPython Methods

**AI overview:**
IPython methods enhance interactive computing in Python, offering features beyond the standard interpreter. Some key methods include:

- Tab Completion:
Simplifies code writing by suggesting attributes and methods of objects or modules as you type.
- Introspection:
Provides detailed information about objects, functions, or modules using ? or ??.
- Magic Commands:
Special commands prefixed with % for tasks like timing code execution (%timeit), running external scripts (%run), or accessing shell commands (!).
- Input Caching:
Stores previous commands and outputs, accessible via _, __, ___ for outputs and _i, _ii, _iii or In[n] for inputs.
- Rich Display:
Enables richer object representations using _ipython_display_() or _repr_*_() methods for custom display formats like HTML or images.
- History:
Allows browsing and reusing previous commands across sessions.
These methods streamline development, debugging, and exploration in interactive Python environments.

References:

- [IPython Reference](https://ipython.org/ipython-doc/3/interactive/reference.html)
  - [Built-in magic commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html)

### Decorators

Code for a caching **decorator** is in
[landmapy/cached.py](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/cached.py),
which you can use in your code.
This decorator will **pickle** the results of running a `do_something()` function,
and only run the code if the results do not already exist.
To override the caching, for example temporarily after
making changes to your code, set `override=True`.
Note that to use the caching decorator, you must write your own function to perform each task.
See examples in
[landmapy/delta.py](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/delta.py)
and
[landmapy/reflectance.py](https://github.com/byandell-envsys/landmapy/blob/main/landmapy/reflectance.py).

- [Clustering Project](https://github.com/earthlab-education/clustering-byandell/blob/main/clustering.qmd)
- [Decorators in Python (Geeks4Geeks)](https://www.geeksforgeeks.org/decorators-in-python/)
- [Primer on Python Decorators (RealPython)](https://realpython.com/primer-on-python-decorators/)
- [PEP 318 – Decorators for Functions and Methods](https://peps.python.org/pep-0318/)
- [Python Decorators with Examples (Programiz)](https://www.programiz.com/python-programming/decorator)

### Classes

A 
[class](https://docs.python.org/3/tutorial/classes.html)
is a function with output of an object that has new methods, which are in turn functions
defined in the class.
In addition, the `@property` decorator defines attributes for the object.
The main use of classes are to:

- add functionality to class
- streamline different functions with same parameters to keep track of metadata

**AI overview:**
In Python, a class serves as a blueprint for creating objects, which are instances that encapsulate data (attributes) and behavior (methods). Classes facilitate object-oriented programming (OOP) principles, enabling code reusability, modularity, and organization.
A class is defined using the class keyword, followed by the class name and a colon. Inside the class block, attributes and methods are defined. The __init__ method is a special method, known as the constructor, which is automatically called when an object of the class is created. It is used to initialize the object's attributes.

- [Habitat Suitability Notes](https://github.com/earthlab-education/habitat-suitability-byandell/blob/main/notes.qmd)
- [Python 3 Documentation](https://docs.python.org/3/)
  - [3. Data model](https://docs.python.org/3/reference/datamodel.html)
  - [9. Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python Classes and Objects (Geeks4Geeks)](https://www.geeksforgeeks.org/python-classes-and-objects/)
- [Python Classes: The Power of Object-Oriented Programming (RealPython)](https://realpython.com/python-classes/)
- [Google's Python Class](https://developers.google.com/edu/python)
- [earthpy](https://earthpy.readthedocs.io/en/latest/)
  - [apppeears.py](https://github.com/earthlab/earthpy/blob/apppears/earthpy/appeears.py) (class Elsa created in `earthpy` package)

### Animated GIFs

- [Creating an Animated GIF with Python](https://www.blog.pythonlibrary.org/2021/06/23/creating-an-animated-gif-with-python/)
  - [Create an Animated GIF Using Python Matplotlib
](https://www.geeksforgeeks.org/create-an-animated-gif-using-python-matplotlib/)
  - [Create a GIF with Python](https://www.codedex.io/projects/create-a-gif-with-python)
  - [Using Python to make an animated gif out of a collection of images](https://propolis.io/articles/make-animated-gif-using-python.html)
  - [How to make a gif map using Python, Geopandas and Matplotlib](https://towardsdatascience.com/how-to-make-a-gif-map-using-python-geopandas-and-matplotlib-cd8827cefbc8)
  - [How to create animated GIF with Pillow in Python](https://note.nkmk.me/en/python-pillow-gif/)
