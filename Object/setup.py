
#cython: language_level=3


from distutils.core import setup
from Cython.Build import cythonize

# use this command: python setup.py build_ext --inplace

# use this command : cython -a World.pyx  to see what does python do for type checking
setup(ext_modules = cythonize("World.pyx",annotate=True))
