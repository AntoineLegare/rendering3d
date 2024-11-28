import numpy as np
from mayavi import mlab
from matplotlib.pyplot import cm
from tvtk.util.ctf import ColorTransferFunction, PiecewiseFunction
import os
import imageio
import nrrd
from tifffile import imread
import shutil
from tqdm import tqdm


def load_stack(path):
    """
    Loads a 3D microscopy (or any other kind of)image stack. Works only for .tif and .nrrd files.
     In the second case, a file header is returned.

    Arguments:
        path (str): Full absolute path of the .tif or .nrrd file.

    Returns:
         array (np.ndarray): 3D umpy array of N-bit values.
         header (dict): Dictionary of image metadata.
    """
    if '.tif' in path:
        return imread(path)
    elif '.nrrd' in path:
        array, metadata = nrrd.read(path)
        array = np.swapaxes(array, 0, 2)
        return array, metadata


class Scene:

    def __init__(self, background_color=(1, 1, 1), size=(1000, 1000), interactive_mode=False, offscreen=False):

        self.bgcolor = background_color
        self.size = size
        self.offscreen = offscreen

        mlab.options.offscreen = self.offscreen
        self.interactive_mode = interactive_mode
        mlab.figure(bgcolor=self.bgcolor, size=self.size)

    def plot_axes(self, color=(0, 0, 0), nb_labels=5, show_orientation=False):
        mlab.axes(
            xlabel='X',
            ylabel='Y',
            zlabel='Z',
            nb_labels=nb_labels,  # Number of labels on each axis
            color=color  # RGB color for the axes
        )
        if show_orientation:
            mlab.orientation_axes()

    def plot_outline(self, color=(0, 0, 0)):
        outline = mlab.outline()
        outline.actor.property.color = color

    def render_stack(self, stack, cmap='binary', vmin=0, vmax=None, opacity=1.0):
        stack_ = np.flip(np.flip(np.swapaxes(stack, 0, 2), axis=0), axis=2)
        if vmax is None:
            vmax = np.max(stack_)
        field = mlab.pipeline.scalar_field(stack_)
        volume = mlab.pipeline.volume(field, vmin=vmin, vmax=vmax)
        self.apply_colormap(cmap, volume, vmin, vmax)
        if opacity != 1:
            self.apply_opacity(volume, opacity, vmin, vmax)
        del stack_

    def render_mask(self, binary_mask, opacity=0.25, color=(1, 1, 1)):
        binary_mask_ = np.flip(np.flip(np.swapaxes(binary_mask, 0, 2), axis=0), axis=2)
        mlab.contour3d(binary_mask_, contours=[1.0],
                       opacity=opacity,
                       color=color)
        del binary_mask_

    def render_points(self, centroids, volume_shape=(359, 974, 597), size=5, color=(1, 0, 0), opacity=1.0):

        mlab.points3d(volume_shape[2] - centroids[:, 0], centroids[:, 1], volume_shape[0] - centroids[:, 2],
                          scale_factor=size,
                          color=color,
                          mode='sphere',
                          opacity=opacity)

    def apply_colormap(self, cmap, volume, vmin, vmax, increments=256):
        ctf = ColorTransferFunction()
        values_array = np.linspace(vmin, vmax, increments)
        values_cmap = np.linspace(0., 1, increments)
        color_mapping = np.append(np.expand_dims(values_array, axis=1), cm.get_cmap(cmap)(values_cmap)[:, :3], axis=1)
        for c in color_mapping:
            ctf.add_rgb_point(c[0], c[1], c[2], c[3])
        volume._volume_property.set_color(ctf)
        volume._ctf = ctf

    def apply_opacity(self, volume, alpha, vmin, vmax):
        otf = PiecewiseFunction()
        otf.add_point(0, 0)
        otf.add_point(vmin - 1, 0)
        otf.add_point(vmin, alpha)
        otf.add_point(vmax, alpha)
        volume._volume_property.set_scalar_opacity(otf)
        volume.update_ctf = True

    def view(self, azimuth=0, elevation=0, distance=2000, preset=None):
        if preset == 'top':
            mlab.view(azimuth=180, elevation=0, distance=distance)
        elif preset == 'side_left':
            mlab.view(azimuth=0, elevation=90, distance=distance)
        elif preset == 'side_right':
            mlab.view(azimuth=180, elevation=90, distance=distance)
        elif preset == 'front':
            mlab.view(azimuth=-90, elevation=90, distance=distance)
        elif preset == 'back':
            mlab.view(azimuth=90, elevation=90, distance=distance)
        else:
            mlab.view(azimuth=azimuth, elevation=elevation, distance=distance)

        if self.interactive_mode:
            mlab.show()
        else:
            mlab.draw()

    def save(self, path, size=None):
        if size is None:
            size = self.size
        if not self.interactive_mode:
            mlab.savefig(path, size=size)

    def generate_gif(self, path, n_frames=360, azimuth_range=(0, 360), elevation_range=(60, 60),
                     distance_range=(2000, 2000), fps=30):
        mlab.draw()
        azimuth_values = np.linspace(azimuth_range[0], azimuth_range[1], n_frames, endpoint=False)
        elevation_values = np.linspace(elevation_range[0], elevation_range[1], n_frames, endpoint=False)
        distance_values = np.linspace(distance_range[0], distance_range[1], n_frames, endpoint=False)

        directory, file_name = os.path.split(path)

        temp_dir = directory + '/temp_rendered_frames/'
        os.makedirs(temp_dir, exist_ok=True)

        print('Rendering gif...')
        for i in tqdm(range(n_frames)):
            mlab.view(azimuth=azimuth_values[i], elevation=elevation_values[i], distance=distance_values[i])
            mlab.savefig(temp_dir + f"frame{i}.png")  # Save the frame
            mlab.draw()

        frames = []
        for i in range(n_frames):
            filename = temp_dir + f"frame{i}.png"
            frames.append(imageio.imread(filename))

        imageio.mimsave(path, frames, fps=fps, loop=0)

        shutil.rmtree(temp_dir)
