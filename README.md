# 3D rendering of microscopy data

All functions are based on the `Mayavi` package and located in `main.py`.

For an example use case, see `script.py`.

# Installation

1. Create a `conda` environment with the packages listed in `requirements.txt`
2. Clone this GitHub repository.
3. Run your own adaptation of the `script.py` file.

# Linux hack

Mayavi sometimes doesn't work on Linux, especially on Ubuntu 22.04. To repair it, enter the following lines in a terminal:

$ cd anaconda3/envs/$ENV/lib
$ mkdir backup  
$ mv libstd* backup  
$ cp /usr/lib/x86_64-linux-gnu/libstdc++.so.6  ./
$ ln -s libstdc++.so.6 libstdc++.so
$ ln -s libstdc++.so.6 libstdc++.so.6.0.19

Here, $ENV corresponds to the name of your virtual environment (for instance, `rendering3d`).

# Author

Antoine Légaré (antoine.legare.1@ulaval.ca)

Please contact me if you have any 3D rendering requests that could be added to the package!


