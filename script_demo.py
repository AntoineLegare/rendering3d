from main import *

"""
Author: Antoine Légaré (antoine.legare.1@ulaval.ca)

This script displays multiple rendering functions in interactive (i.e. graphical interface) mode, simultaneously.

The displayed elements are:
  - 3D rendering of a raw microscopy stack
  - 3D rendering of binary brain region/outline masks
  - Scattering of 3D neuron coordinates as little spheres
  
This script intentionally displays too many things. For use with your own data, copy the script, change paths, and
remove any unwanted elements. Feel free to tweak parameters below (for instance, stack colormap, azimuth and elevation
of the camera view, etc).

To render a .png image instead of opening the interactive GUI, simply change 'interactive_mode' to False, 'save_frame'
to True, and provide a path for the output .png image in 'frame_path' (don't forget the file extension).

Similarly, to generate a nice video of a rotating 3D rendering, change 'interactive_mode' to False, 'save_gif' to True,
and provide a path (in .gif extension). It is recommended to set 'offscreen' to True for this option, as the GUI
rendering is heavy.

If you ever interrupt the .gif rendering, delete the 'temp_rendered_frames' folder that is generated temporarily.

Have fun!
"""

# ----------------------------------------------------------------------------------------------------------------------
# Loading data

path = '/home/anleg84/Documents/Atlas/Rendering/'

stack = load_stack(path + 'template.tif')
mask_wholebrain = load_stack(path + 'mask_wholebrain.tif')
mask_tectum = load_stack(path + 'mask_tectum.tif')
centroids = np.load(path + 'centroids.npy')

# ----------------------------------------------------------------------------------------------------------------------
# Toggling interactive mode and file saves

interactive_mode = False  # Put False if saving any output
offscreen = True         # Put to True to render frames off-screen (no GUI). Preferable for .gif output.

save_frame = False
frame_path = '/home/anleg84/GitHub/rendering3d/frame.png'

save_gif = True
gif_path = '/home/anleg84/GitHub/rendering3d/rotation.gif'

# ----------------------------------------------------------------------------------------------------------------------
# Rendering the scene

scene = Scene(background_color=(1, 1, 1),
              size=(1000, 1000),
              interactive_mode=interactive_mode,
              offscreen=offscreen
              )

scene.render_stack(stack,
                   vmin=50,  # Anything below this value is not displayed at all
                   vmax=255,  # Anything above this value is saturated
                   cmap='binary',     # Search 'matplotlib colormaps' for full list
                   opacity=0.005
                   )

scene.render_mask(mask_wholebrain,
                  opacity=0.25,
                  color=(1, 1, 1)
                  )

scene.render_mask(mask_tectum,
                  opacity=0.25,
                  color=(1, 0, 0)
                  )

scene.render_points(centroids,
                    volume_shape=(359, 974, 597),  # S (z, y, x) volume shape; adjust for different shapes
                    size=5,
                    color=(1, 0, 1),
                    opacity=1.0
                    )

scene.view(azimuth=-30,
           elevation=60,
           distance=2000,
           preset=None  # Available presets are 'top', 'side_right', 'side_left', 'front', 'back'
           )

if save_frame:
    scene.save(frame_path)

if save_gif:
    scene.generate_gif(gif_path,
                       n_frames=360,
                       azimuth_range=(0, 360),
                       elevation_range=(60, 60),
                       distance_range=(2000, 2000),
                       fps=30,
                       )
