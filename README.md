# 3D rendering of microscopy data

Simple Python code to render 3D microscopy data.

All functions are based on the `Mayavi` package and located in `main.py`.

For an example use case, see `script_demo.py`.

# Installation

1. Create a `conda` environment with the packages listed in `requirements.txt`
2. Clone this GitHub repository.
3. Run your own adaptation of the `script.py` file.

**Note**: The requirements provided here are rough guidelines of package versions that worked on a single machine. Some installations worked with Python 3.7, others with Python 3.9, depending on the computer and OS. Package versions may change, and you may want to install from scratch, starting with `pip install mayavi`, and working your way up the package list. Mayavi may get version incompatibilities with Numpy (for instance, by installing Numpy >2.0), which will result in binary errors during imports. Numpy 1.26.0 seems to be a good fit, regardless of the version.

# Linux hack

Mayavi sometimes doesn't work on Linux due to external dependencies, especially on Ubuntu 22.04. To repair it (if there are errors), enter the following lines in a terminal:

`cd anaconda3/envs/$ENV/lib`

`mkdir backup`

`mv libstd* backup`

`cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6  ./`

`ln -s libstdc++.so.6 libstdc++.so`

`ln -s libstdc++.so.6 libstdc++.so.6.0.19`

Here, `$ENV` corresponds to the name of your virtual environment (for instance, `rendering`).

# Author

Antoine Légaré (antoine.legare.1@ulaval.ca)

Please contact me if you have any 3D rendering requests that could be added to the package!


