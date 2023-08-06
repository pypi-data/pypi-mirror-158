import logging
import numpy as np
import copy
from typing import List, Optional

from autoconf import cached_property

from autoarray.dataset.abstract_dataset import AbstractWTilde
from autoarray.dataset.abstract_dataset import AbstractSettingsDataset
from autoarray.dataset.abstract_dataset import AbstractDataset
from autoarray.mask.mask_2d import Mask2D
from autoarray.structures.grids.uniform_2d import Grid2D
from autoarray.operators.transformer import TransformerDFT
from autoarray.operators.transformer import TransformerNUFFT
from autoarray.structures.visibilities import Visibilities
from autoarray.structures.visibilities import VisibilitiesNoiseMap

from autoarray import exc
from autoarray.structures.arrays import array_2d_util
from autoarray.dataset import preprocess

logger = logging.getLogger(__name__)


class WTildeInterferometer(AbstractWTilde):
    def __init__(
        self,
        w_matrix: np.ndarray,
        curvature_preload: np.ndarray,
        dirty_image: np.ndarray,
        real_space_mask: Mask2D,
        noise_map_value: float,
    ):
        """
        Packages together all derived data quantities necessary to fit `Interferometer` data using an ` Inversion` via
        the w_tilde formalism.

        The w_tilde formalism performs linear algebra formalism in a way that speeds up the construction of  the
        simultaneous linear equations by bypassing the construction of a `mapping_matrix` and precomputing the
        Fourier transform operations performed using the interferometer's `uv_wavelengths`.

        Parameters
        ----------
        w_matrix
            The w_tilde matrix used to construct the data vector during an inversion.
        curvature_preload
            A matrix which uses the interferometer `uv_wavelengths` to preload as much of the computation of the
            curvature matrix as possible.
        dirty_image
            The real-space image of the visibilities computed via the transform, which is used to construct the
            curvature matrix.
        real_space_mask
            The 2D mask in real-space defining the area where the interferometer data's visibilities are observing
            a signal.
        noise_map_value
            The first value of the noise-map used to construct the curvature preload, which is used as a sanity
            check when performing the inversion to ensure the preload corresponds to the data being fitted.
        """
        super().__init__(
            curvature_preload=curvature_preload, noise_map_value=noise_map_value
        )

        self.dirty_image = dirty_image
        self.real_space_mask = real_space_mask

        self.w_matrix = w_matrix


class SettingsInterferometer(AbstractSettingsDataset):
    def __init__(
        self,
        grid_class=Grid2D,
        grid_pixelized_class=Grid2D,
        sub_size: int = 1,
        sub_size_pixelized=1,
        fractional_accuracy: float = 0.9999,
        sub_steps: List[int] = None,
        signal_to_noise_limit: Optional[float] = None,
        transformer_class=TransformerNUFFT,
    ):
        """
          The lens dataset is the collection of data_type (image, noise-map), a mask, grid, convolver \
          and other utilities that are used for modeling and fitting an image of a strong lens.

          Whilst the image, noise-map, etc. are loaded in 2D, the lens dataset creates reduced 1D arrays of each \
          for lens calculations.

          Parameters
          ----------
        grid_class : ag.Grid2D
            The type of grid used to create the image from the `Galaxy` and `Plane`. The options are `Grid2D`,
            and `Grid2DIterate` (see the `Grid2D` documentation for a description of these options).
        grid_pixelized_class : ag.Grid2D
            The type of grid used to create the grid that maps the `LEq` source pixels to the data's image-pixels.
            The options are `Grid2D` and `Grid2DIterate` (see the `Grid2D` documentation for a
            description of these options).
        sub_size
            If the grid and / or grid_pixelized use a `Grid2D`, this sets the sub-size used by the `Grid2D`.
        fractional_accuracy
            If the grid and / or grid_pixelized use a `Grid2DIterate`, this sets the fractional accuracy it
            uses when evaluating functions.
        sub_steps : [int]
            If the grid and / or grid_pixelized use a `Grid2DIterate`, this sets the steps the sub-size is increased by
            to meet the fractional accuracy when evaluating functions.
        signal_to_noise_limit
            If input, the dataset's noise-map is rescaled such that no pixel has a signal-to-noise above the
            signa to noise limit.
          """

        super().__init__(
            grid_class=grid_class,
            grid_pixelized_class=grid_pixelized_class,
            sub_size=sub_size,
            sub_size_pixelized=sub_size_pixelized,
            fractional_accuracy=fractional_accuracy,
            sub_steps=sub_steps,
            signal_to_noise_limit=signal_to_noise_limit,
        )

        self.transformer_class = transformer_class


class Interferometer(AbstractDataset):
    def __init__(
        self,
        visibilities: Visibilities,
        noise_map: VisibilitiesNoiseMap,
        uv_wavelengths: np.ndarray,
        real_space_mask,
        settings=SettingsInterferometer(),
        name=None,
    ):

        self.real_space_mask = real_space_mask

        super().__init__(
            data=visibilities, noise_map=noise_map, name=name, settings=settings
        )

        self.uv_wavelengths = uv_wavelengths

        self.transformer = self.settings.transformer_class(
            uv_wavelengths=uv_wavelengths, real_space_mask=real_space_mask
        )

    @classmethod
    def from_fits(
        cls,
        visibilities_path,
        noise_map_path,
        uv_wavelengths_path,
        real_space_mask,
        visibilities_hdu=0,
        noise_map_hdu=0,
        uv_wavelengths_hdu=0,
        settings=SettingsInterferometer(),
    ):
        """Factory for loading the interferometer data_type from .fits files, as well as computing properties like the noise-map,
        exposure-time map, etc. from the interferometer-data_type.

        This factory also includes a number of routines for converting the interferometer-data_type from unit_label not supported by PyAutoLens \
        (e.g. adus, electrons) to electrons per second.

        Parameters
        ----------
        """

        visibilities = Visibilities.from_fits(
            file_path=visibilities_path, hdu=visibilities_hdu
        )

        noise_map = VisibilitiesNoiseMap.from_fits(
            file_path=noise_map_path, hdu=noise_map_hdu
        )

        uv_wavelengths = array_2d_util.numpy_array_2d_via_fits_from(
            file_path=uv_wavelengths_path, hdu=uv_wavelengths_hdu
        )

        return Interferometer(
            real_space_mask=real_space_mask,
            visibilities=visibilities,
            noise_map=noise_map,
            uv_wavelengths=uv_wavelengths,
            settings=settings,
        )

    def apply_settings(self, settings):

        return Interferometer(
            visibilities=self.visibilities,
            noise_map=self.noise_map,
            uv_wavelengths=self.uv_wavelengths,
            real_space_mask=self.real_space_mask,
            settings=settings,
            name=self.name,
        )

    @cached_property
    def w_tilde(self):
        """
        The w_tilde formalism of the linear algebra equations precomputes the Fourier Transform of all the visibilities
        given the `uv_wavelengths` (see `inversion.inversion_util`).

        The `WTilde` object stores these precomputed values in the interferometer dataset ensuring they are only
        computed once per analysis.

        This uses lazy allocation such that the calculation is only performed when the wtilde matrices are used,
        ensuring efficient set up of the `Interferometer` class.

        Returns
        -------
        WTildeInterferometer
            Precomputed values used for the w tilde formalism of linear algebra calculations.
        """

        from autoarray.inversion.inversion import inversion_util_secret

        logger.info("INTERFEROMETER - Computing W-Tilde... May take a moment.")

        curvature_preload = inversion_util_secret.w_tilde_curvature_preload_interferometer_from(
            noise_map_real=self.noise_map.real,
            uv_wavelengths=self.uv_wavelengths,
            shape_masked_pixels_2d=self.transformer.grid.mask.shape_native_masked_pixels,
            grid_radians_2d=self.transformer.grid.mask.unmasked_grid_sub_1.in_radians.native,
        )

        w_matrix = inversion_util_secret.w_tilde_via_preload_from(
            w_tilde_preload=curvature_preload,
            native_index_for_slim_index=self.real_space_mask.native_index_for_slim_index,
        )

        dirty_image = self.transformer.image_from(
            visibilities=self.visibilities.real * self.noise_map.real ** -2.0
            + 1j * self.visibilities.imag * self.noise_map.imag ** -2.0,
            use_adjoint_scaling=True,
        )

        return WTildeInterferometer(
            w_matrix=w_matrix,
            curvature_preload=curvature_preload,
            dirty_image=dirty_image,
            real_space_mask=self.real_space_mask,
            noise_map_value=self.noise_map[0],
        )

    @property
    def mask(self):
        return self.real_space_mask

    @property
    def visibilities(self):
        return self.data

    @property
    def amplitudes(self):
        return self.visibilities.amplitudes

    @property
    def phases(self):
        return self.visibilities.phases

    @property
    def uv_distances(self):
        return np.sqrt(
            np.square(self.uv_wavelengths[:, 0]) + np.square(self.uv_wavelengths[:, 1])
        )

    @property
    def dirty_image(self):
        return self.transformer.image_from(visibilities=self.visibilities)

    @property
    def dirty_noise_map(self):
        return self.transformer.image_from(visibilities=self.noise_map)

    @property
    def dirty_signal_to_noise_map(self):
        return self.transformer.image_from(visibilities=self.signal_to_noise_map)

    @property
    def dirty_inverse_noise_map(self):
        return self.transformer.image_from(visibilities=self.inverse_noise_map)

    @property
    def signal_to_noise_map(self):

        signal_to_noise_map_real = np.divide(
            np.real(self.data), np.real(self.noise_map)
        )
        signal_to_noise_map_real[signal_to_noise_map_real < 0] = 0.0
        signal_to_noise_map_imag = np.divide(
            np.imag(self.data), np.imag(self.noise_map)
        )
        signal_to_noise_map_imag[signal_to_noise_map_imag < 0] = 0.0

        return signal_to_noise_map_real + 1j * signal_to_noise_map_imag

    @property
    def blurring_grid(self):
        return None

    @property
    def convolver(self):
        return None

    def signal_to_noise_limited_from(self, signal_to_noise_limit, mask=None):

        interferometer = copy.deepcopy(self)

        noise_map_limit_real = np.where(
            np.real(self.signal_to_noise_map) > signal_to_noise_limit,
            np.real(self.visibilities) / signal_to_noise_limit,
            np.real(self.noise_map),
        )

        noise_map_limit_imag = np.where(
            np.imag(self.signal_to_noise_map) > signal_to_noise_limit,
            np.imag(self.visibilities) / signal_to_noise_limit,
            np.imag(self.noise_map),
        )

        interferometer.noise_map = VisibilitiesNoiseMap(
            visibilities=noise_map_limit_real + 1j * noise_map_limit_imag
        )

        return interferometer

    def output_to_fits(
        self,
        visibilities_path=None,
        noise_map_path=None,
        uv_wavelengths_path=None,
        overwrite=False,
    ):

        if visibilities_path is not None:
            self.visibilities.output_to_fits(
                file_path=visibilities_path, overwrite=overwrite
            )

        if self.noise_map is not None and noise_map_path is not None:
            self.noise_map.output_to_fits(file_path=noise_map_path, overwrite=overwrite)

        if self.uv_wavelengths is not None and uv_wavelengths_path is not None:
            array_2d_util.numpy_array_2d_to_fits(
                array_2d=self.uv_wavelengths,
                file_path=uv_wavelengths_path,
                overwrite=overwrite,
            )


class AbstractSimulatorInterferometer:
    def __init__(
        self,
        uv_wavelengths,
        exposure_time: float,
        transformer_class=TransformerDFT,
        noise_sigma=0.1,
        noise_if_add_noise_false=0.1,
        noise_seed=-1,
    ):
        """A class representing a Imaging observation, using the shape of the image, the pixel scale,
        psf, exposure time, etc.

        Parameters
        ----------
        real_space_shape_native
            The shape of the observation. Note that we do not simulator a full Imaging array (e.g. 2000 x 2000 pixels for \
            Hubble imaging), but instead just a cut-out around the strong lens.
        real_space_pixel_scales
            The size of each pixel in scaled units.
        psf : PSF
            An arrays describing the PSF kernel of the image.
        exposure_time_map
            The exposure time of an observation using this data_type.
        """

        self.uv_wavelengths = uv_wavelengths
        self.exposure_time = exposure_time
        self.transformer_class = transformer_class
        self.noise_sigma = noise_sigma
        self.noise_if_add_noise_false = noise_if_add_noise_false
        self.noise_seed = noise_seed

    def via_image_from(self, image, name=None):
        """
        Returns a realistic simulated image by applying effects to a plain simulated image.

        Parameters
        ----------
        name
        real_space_image
            The image before simulating (e.g. the lens and source galaxies before optics blurring and UVPlane read-out).
        real_space_pixel_scales
            The scale of each pixel in scaled units
        exposure_time_map
            An array representing the effective exposure time of each pixel.
        psf: PSF
            An array describing the PSF the simulated image is blurred with.
        add_poisson_noise: Bool
            If `True` poisson noise_maps is simulated and added to the image, based on the total counts in each image
            pixel
        noise_seed: int
            A seed for random noise_maps generation
        """

        transformer = self.transformer_class(
            uv_wavelengths=self.uv_wavelengths, real_space_mask=image.mask
        )

        visibilities = transformer.visibilities_from(image=image)

        if self.noise_sigma is not None:
            visibilities = preprocess.data_with_complex_gaussian_noise_added(
                data=visibilities, sigma=self.noise_sigma, seed=self.noise_seed
            )
            noise_map = VisibilitiesNoiseMap.full(
                fill_value=self.noise_sigma, shape_slim=(visibilities.shape[0],)
            )
        else:
            noise_map = VisibilitiesNoiseMap.full(
                fill_value=self.noise_if_add_noise_false,
                shape_slim=(visibilities.shape[0],),
            )

        if np.isnan(noise_map).any():
            raise exc.DatasetException(
                "The noise-map has NaN values in it. This suggests your exposure time and / or"
                "background sky levels are too low, creating signal counts at or close to 0.0."
            )

        return Interferometer(
            visibilities=visibilities,
            noise_map=noise_map,
            uv_wavelengths=transformer.uv_wavelengths,
            real_space_mask=image.mask,
            name=name,
        )


class SimulatorInterferometer(AbstractSimulatorInterferometer):

    pass
