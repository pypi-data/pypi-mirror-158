import numpy as np
from scipy.linalg import cho_solve

from autoarray.inversion.inversion.settings import SettingsInversion

from autoarray import numba_util
from autoarray import exc

from autoarray.inversion.linear_eqn import leq_util


def reconstruction_from(
    data_vector: np.ndarray,
    curvature_reg_matrix_cholesky: np.ndarray,
    settings: SettingsInversion = SettingsInversion(),
):
    """
    Solve the linear system [F + reg_coeff*H] S = D -> S = [F + reg_coeff*H]^-1 D given by equation (12)
    of https://arxiv.org/pdf/astro-ph/0302587.pdf

    S is the vector of reconstructed inversion values.

    This function checks that the solution does not give a linear algebra error (e.g. because the input matrix is
    not positive-definitive) and that it avoids solutions where all reconstructed values go to the same value. If these
    occur it raises an exception.

    Parameters
    ----------
    data_vector
        The `data_vector` D which is solved for.
    curvature_reg_matrix_cholesky
        The cholesky decomposition of the sum of the curvature and regularization matrices.
    settings
        Controls the settings of the inversion, for this function where the solution is checked to not be all
        the same values.

    Returns
    -------
    curvature_reg_matrix
        The curvature_matrix plus regularization matrix, overwriting the curvature_matrix in memory.
    """
    try:
        reconstruction = cho_solve((curvature_reg_matrix_cholesky, True), data_vector)
    except np.linalg.LinAlgError:
        raise exc.InversionException()

    if settings.check_solution and len(reconstruction) > 1:
        if np.isclose(a=reconstruction[0], b=reconstruction[1], atol=1e-4).all():
            if np.isclose(a=reconstruction[0], b=reconstruction, atol=1e-4).all():
                raise exc.InversionException()

    return reconstruction


def preconditioner_matrix_via_mapping_matrix_from(
    mapping_matrix: np.ndarray,
    regularization_matrix: np.ndarray,
    preconditioner_noise_normalization: float,
) -> np.ndarray:
    """
    Returns the preconditioner matrix `{` from a mapping matrix `f` and the sum of the inverse of the 1D noise-map
    values squared (see Powell et al. 2020).

    Parameters
    -----------
    mapping_matrix
        The matrix representing the mappings between sub-grid pixels and pixelization pixels.
    regularization_matrix
        The matrix defining how the pixelization's pixels are regularized with one another for smoothing (H).
    preconditioner_noise_normalization
        The sum of (1.0 / noise-map**2.0) every value in the noise-map.
    """

    curvature_matrix = leq_util.curvature_matrix_via_mapping_matrix_from(
        mapping_matrix=mapping_matrix,
        noise_map=np.ones(shape=(mapping_matrix.shape[0])),
    )

    return (
        preconditioner_noise_normalization * curvature_matrix
    ) + regularization_matrix


def inversion_residual_map_from(
    *,
    reconstruction: np.ndarray,
    data: np.ndarray,
    slim_index_for_sub_slim_index: np.ndarray,
    sub_slim_indexes_for_pix_index: [list],
):
    """
    Returns the residual-map of the `reconstruction` of an `LEq` on its pixel-grid.

    For this residual-map, each pixel on the `reconstruction`'s pixel-grid corresponds to the sum of absolute residual
    values in the `residual_map` of the reconstructed `data` divided by the number of data-points that it maps too,
    (to normalize its value).

    This provides information on where in the `LEq`'s `reconstruction` it is least able to accurately fit the
    `data`.

    Parameters
    ----------
    reconstruction
        The values computed by the `LEq` for the `reconstruction`, which are used in this function to compute
        the `residual_map` values.
    data
        The array of `data` that the `LEq` fits.
    slim_index_for_sub_slim_index
        The mappings between the observed grid's sub-pixels and observed grid's pixels.
    sub_slim_indexes_for_pix_index
        The mapping of every pixel on the `LinearEqn`'s `reconstruction`'s pixel-grid to the `data` pixels.

    Returns
    -------
    np.ndarray
        The residuals of the `LEq`'s `reconstruction` on its pixel-grid, computed by mapping the `residual_map`
        from the fit to the data.
    """
    residual_map = np.zeros(shape=len(sub_slim_indexes_for_pix_index))

    for pix_index, sub_slim_indexes in enumerate(sub_slim_indexes_for_pix_index):

        sub_mask_total = 0
        for sub_mask_1d_index in sub_slim_indexes:
            sub_mask_total += 1
            mask_1d_index = slim_index_for_sub_slim_index[sub_mask_1d_index]
            residual = data[mask_1d_index] - reconstruction[pix_index]
            residual_map[pix_index] += np.abs(residual)

        if sub_mask_total > 0:
            residual_map[pix_index] /= sub_mask_total

    return residual_map.copy()


def inversion_normalized_residual_map_from(
    *,
    reconstruction,
    data,
    noise_map_1d,
    slim_index_for_sub_slim_index,
    sub_slim_indexes_for_pix_index,
):
    """
    Returns the normalized residual-map of the `reconstruction` of an `LEq` on its pixel-grid.

    For this normalized residual-map, each pixel on the `reconstruction`'s pixel-grid corresponds to the sum of
    absolute normalized residual values in the `normalized residual_map` of the reconstructed `data` divided by the
    number of data-points that it maps too (to normalize its value).

    This provides information on where in the `LEq`'s `reconstruction` it is least able to accurately fit the
    `data`.

    Parameters
    ----------
    reconstruction
        The values computed by the `LEq` for the `reconstruction`, which are used in this function to compute
        the `normalized residual_map` values.
    data
        The array of `data` that the `LEq` fits.
    slim_index_for_sub_slim_index
        The mappings between the observed grid's sub-pixels and observed grid's pixels.
    sub_slim_indexes_for_pix_index
        The mapping of every pixel on the `LinearEqn`'s `reconstruction`'s pixel-grid to the `data` pixels.

    Returns
    -------
    np.ndarray
        The normalized residuals of the `LEq`'s `reconstruction` on its pixel-grid, computed by mapping the
        `normalized_residual_map` from the fit to the data.
    """
    normalized_residual_map = np.zeros(shape=len(sub_slim_indexes_for_pix_index))

    for pix_index, sub_slim_indexes in enumerate(sub_slim_indexes_for_pix_index):
        sub_mask_total = 0
        for sub_mask_1d_index in sub_slim_indexes:
            sub_mask_total += 1
            mask_1d_index = slim_index_for_sub_slim_index[sub_mask_1d_index]
            residual = data[mask_1d_index] - reconstruction[pix_index]
            normalized_residual_map[pix_index] += np.abs(
                (residual / noise_map_1d[mask_1d_index])
            )

        if sub_mask_total > 0:
            normalized_residual_map[pix_index] /= sub_mask_total

    return normalized_residual_map.copy()


def inversion_chi_squared_map_from(
    *,
    reconstruction,
    data,
    noise_map_1d,
    slim_index_for_sub_slim_index,
    sub_slim_indexes_for_pix_index,
):
    """
    Returns the chi-squared-map of the `reconstruction` of an `LEq` on its pixel-grid.

    For this chi-squared-map, each pixel on the `reconstruction`'s pixel-grid corresponds to the sum of chi-squared
    values in the `chi_squared_map` of the reconstructed `data` divided by the number of data-points that it maps too,
    (to normalize its value).

    This provides information on where in the `LEq`'s `reconstruction` it is least able to accurately fit the
    `data`.

    Parameters
    ----------
    reconstruction
        The values computed by the `LEq` for the `reconstruction`, which are used in this function to compute
        the `chi_squared_map` values.
    data
        The array of `data` that the `LEq` fits.
    slim_index_for_sub_slim_index
        The mappings between the observed grid's sub-pixels and observed grid's pixels.
    sub_slim_indexes_for_pix_index
        The mapping of every pixel on the `LinearEqn`'s `reconstruction`'s pixel-grid to the `data` pixels.

    Returns
    -------
    np.ndarray
        The chi-squareds of the `LEq`'s `reconstruction` on its pixel-grid, computed by mapping the `chi-squared_map`
        from the fit to the data.
    """
    chi_squared_map = np.zeros(shape=len(sub_slim_indexes_for_pix_index))

    for pix_index, sub_slim_indexes in enumerate(sub_slim_indexes_for_pix_index):
        sub_mask_total = 0
        for sub_mask_1d_index in sub_slim_indexes:
            sub_mask_total += 1
            mask_1d_index = slim_index_for_sub_slim_index[sub_mask_1d_index]
            residual = data[mask_1d_index] - reconstruction[pix_index]
            chi_squared_map[pix_index] += (
                residual / noise_map_1d[mask_1d_index]
            ) ** 2.0

        if sub_mask_total > 0:
            chi_squared_map[pix_index] /= sub_mask_total

    return chi_squared_map.copy()
