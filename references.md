# Python References

This is a collection of Python references that I have found useful.
See related in
[EDA References](https://github.com/byandell-envsys/EarthDataAnalytics/blob/main/references.md).
Please offer suggestions to improve.

- [Python References](#python-references)
  - [Python Overview](#python-overview)
  - [Earth Data Analytics (EDA) Workbook](#earth-data-analytics-eda-workbook)
  - [Useful Python Libraries](#useful-python-libraries)
    - [Lists of Python Libraries](#lists-of-python-libraries)
  - [Plot Libraries and Systems](#plot-libraries-and-systems)
    - [Spatial Libraries](#spatial-libraries)
    - [Animated GIFs](#animated-gifs)
  - [IPython Methods](#ipython-methods)
    - [Decorators](#decorators)
    - [Classes](#classes)

## Python Overview

- [Python Tutorial](https://docs.python.org/3/tutorial/)
  - [Modules](https://docs.python.org/3/tutorial/modules.html)
  - [Importing Modules](https://docs.python.org/3/reference/import.html)
  - [Packages](https://docs.python.org/3/tutorial/modules.html#packages)
- [Pandas Library](https://pandas.pydata.org/docs/)
  - [Pandas Tutorial](https://pandas.pydata.org/docs/user_guide/10min.html)
  - [Pandas API Reference](https://pandas.pydata.org/docs/reference/)
- [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Try and Except code for NetCDF](https://www.earthdatascience.org/courses/use-data-open-source-python/hierarchical-data-formats-hdf/get-maca-2-climate-data-netcdf-python/);
- [Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code/)
  - [Hitchhikers Guide to Documentation](https://docs.python-guide.org/writing/documentation/)
    - [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/#introduction)
    - [PEP 257: Docstring Conventions](https://peps.python.org/pep-0257/)
  - [Documentation in Python: Methods and Best Practices](https://swimm.io/learn/code-documentation/documentation-in-python-methods-and-best-practices)
- [Python Developer’s Guide](https://devguide.python.org/)
- [Integrating Python Code With R](https://www.geeksforgeeks.org/integrating-python-code-with-r/)

## Earth Data Analytics (EDA) Workbook

- [Earth Data Analytics (EDA) Workbook](#earth-data-analytics-eda-workbook)
- [EDA Scientific Data Structures in Python](https://www.earthdatascience.org/courses/intro-to-earth-data-science/scientific-data-structures-python/)
- [Subtract One Raster from Another and Export a New GeoTIFF in Open Source Python](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-raster-data-python/raster-data-processing/subtract-rasters-in-python/)
- [Earth Analytics Python Env](https://github.com/earthlab/earth-analytics-python-env)
  -  [EDA 4. Set Up Your Conda Earth Analytics Python Environment Setup earth analytics environment](https://www.earthdatascience.org/workshops/setup-earth-analytics-python/setup-python-conda-earth-analytics-environment/)
      - [Python venv: How To Create, Activate, Deactivate, And Delete](https://python.land/virtual-environments/virtualenv) 
  - [EDA 6.15. Intro to Pandas Dataframes](https://www.earthdatascience.org/courses/intro-to-earth-data-science/scientific-data-structures-python/pandas-dataframes/)

## Useful Python Libraries

- [pandas](https://pandas.pydata.org/)
- [numpy](https://numpy.org/)
- [math](https://docs.python.org/3/library/math.html)
- [time](https://docs.python.org/3/library/time.html)
- [glob](https://docs.python.org/3/library/glob.html)
- [os](https://docs.python.org/3/library/os.html)
- [re](https://docs.python.org/3/library/re.html)
- [csv](https://docs.python.org/3/library/csv.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [zipfile](https://docs.python.org/3/library/zipfile.html)
- [warnings](https://docs.python.org/3/library/warnings.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
- [scipy](https://www.scipy.org/)
- [scikit-fuzzy](https://pythonhosted.org/scikit-fuzzy/)
- [sklearn](https://scikit-learn.org/) (scikit-learn)
  - [sklearn.model_selection](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.model_selection)
  - [sklearn.metrics](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics)
  - [sklearn.cluster](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.cluster)
  - [sklearn.tree](https://scikit-learn.org/stable/modules/classes.html#module-sklearn.tree)
- [seaborn](https://seaborn.pydata.org/)
- [statsmodels](https://www.statsmodels.org/)
- [pystac_client](https://pystac-client.readthedocs.io/en/latest/)
- [pystac](https://pystac.readthedocs.io/en/latest/)

### Lists of Python Libraries

- [The Python Standard Library](https://docs.python.org/3/library/)
- [Python Libraries](https://www.python.org/about/apps/)
- [Awesome Python](https://awesome-python.com/)
- Fan Lists
  - [Geeks4Geeks](https://www.geeksforgeeks.org/python-libraries-to-know/)
  - [dev.to/taipy](https://dev.to/taipy/top-42-python-libraries-you-need-to-know-1omo)
  - [hackr.io](https://hackr.io/blog/best-python-libraries)
  - [Great Learning](https://www.mygreatlearning.com/blog/open-source-python-libraries/)

## Plot Libraries and Systems

- [matplotlib](https://matplotlib.org/)
  - [matplotlib.pyplot](https://matplotlib.org/stable/api/pyplot_api.html)
  - [matplotlib.colors](https://matplotlib.org/stable/api/colors_api.html)
  - [matplotlib.widgets](https://matplotlib.org/stable/api/widgets_api.html) (`%matplotlib widget`)
- [shapely](https://shapely.readthedocs.io/en/stable/)
  - [shapely.geometry](https://shapely.readthedocs.io/en/stable/manual.html#geometric-objects)
- [HoloViews](https://holoviews.org/)
- [GeoViews](https://geoviews.org/)
- [contextily](https://contextily.readthedocs.io/en/latest/)
- [panel](https://panel.holoviz.org/)
- [hvplot](https://hvplot.holoviz.org/)
  - [hvplot.pandas](https://hvplot.holoviz.org/user_guide/Plotting_with_Pandas.html)
  - [hvplot.xarray](https://hvplot.holoviz.org/user_guide/Plotting_with_XArray.html)

### Spatial Libraries

- [geopandas](https://geopandas.org/)
- [rasterio](https://rasterio.readthedocs.io/)
- [xarray](http://xarray.pydata.org/en/)
- [rioxarray](https://corteva.github.io/rioxarray/stable/)
- [xrspatial](https://xarray-spatial.readthedocs.io/en/stable/)
- [earthaccess](https://earthaccess.readthedocs.io/en/latest/)
- [getpass](https://docs.python.org/3/library/getpass.html)
- [earthpy](https://earthpy.readthedocs.io/en/latest/)
- [tqdm](https://tqdm.github.io/)
  - [tqdm.notebook](https://tqdm.github.io/docs/notebook/)
- [regionmask](https://regionmask.readthedocs.io/en/stable/)
- [cartopy](https://scitools.org.uk/cartopy/docs/latest/)
  - [cartopy.crs](https://scitools.org.uk/cartopy/docs/latest/crs/index.html)

### Animated GIFs

- [Creating an Animated GIF with Python](https://www.blog.pythonlibrary.org/2021/06/23/creating-an-animated-gif-with-python/)
  - [Create an Animated GIF Using Python Matplotlib](https://www.geeksforgeeks.org/create-an-animated-gif-using-python-matplotlib/)
  - [Create a GIF with Python](https://www.codedex.io/projects/create-a-gif-with-python)
  - [Using Python to make an animated gif out of a collection of images](https://propolis.io/articles/make-animated-gif-using-python.html)
  - [How to make a gif map using Python, Geopandas and Matplotlib](https://towardsdatascience.com/how-to-make-a-gif-map-using-python-geopandas-and-matplotlib-cd8827cefbc8)
  - [How to create animated GIF with Pillow in Python](https://note.nkmk.me/en/python-pillow-gif/)
- [HoloViews Overview](https://dash.plotly.com/holoviews)
  - [HoloViews Gridded Dataset](https://holoviews.org/user_guide/Gridded_Datasets.html)
  - [HV Gridded getting started](https://holoviews.org/getting_started/Gridded_Datasets.html)
  - [slider](https://stackoverflow.com/questions/76318661/holoviews-interactive-plot-of-gridded-data-with-slider-on-top)
  - [Interactive plots using hvplot](https://tutorial.xarray.dev/intermediate/hvplot.html)
  - [Dimensioned Containers](https://holoviews.org/user_guide/Dimensioned_Containers.html)
  
## IPython Methods

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
  - [Interactive Computing](https://ipython.org/ipython-doc/3/interactive/tutorial.html)

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
