from scipy.stats import expon, lognorm, norm, triang, uniform
import numpy as np


def param_stoiip(
    df,
    row,
    dist_col,
    loc_col,
    scale_col,
    iter,
    sc_col=None,
    lim_min_col=None,
    lim_max_col=None,
    seed=None,
):
    """
    This function has as a goal, return numpy arrays of any stoiip variable like area,
    thickness, porosity, oil saturation and Boi. Furthermore, this numpy array contains
    random variables from various continuous distributions.

    Parameters
    ----------
    df
        Pandas dataframe
    row
        row index
    dist_col
        distribution column
    loc_col
        loc argument column from scipy
    scale_col
        scale argument column from scipy
    sc_col
        c or s argument column from scipy
    lim_min_col
        Minimum limit column
    lim_max_col
        Maximin limit column
    iter
        Number of random variables
    seed
        Specifies the seed number to create the random number generator

    Returns
    -------
    numpy array of the any Stoiip parameter

    """

    if seed is None:
        rng = np.random.default_rng()
    else:
        rng = np.random.default_rng(seed)

    if df.loc[row, dist_col] == "Log-Normal" or df.loc[row, dist_col] == "Triangular":
        if df.loc[row, dist_col] == "Log-Normal":
            param = lognorm.rvs(
                s=df.loc[row, sc_col],
                loc=df.loc[row, loc_col],
                scale=df.loc[row, scale_col],
                size=iter,
                random_state=rng,
            )
            param = np.where(
                param < df.loc[row, lim_min_col], df.loc[row, lim_min_col], param
            )
            param = np.where(
                param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param
            )

        elif df.loc[row, dist_col] == "Triangular":
            param = triang.rvs(
                c=df.loc[row, sc_col],
                loc=df.loc[row, loc_col],
                scale=df.loc[row, scale_col],
                size=iter,
                random_state=rng,
            )

    elif df.loc[row, dist_col] == "Normal":
        param = norm.rvs(
            loc=df.loc[row, loc_col],
            scale=df.loc[row, scale_col],
            size=iter,
            random_state=rng,
        )
        param = np.where(
            param < df.loc[row, lim_min_col], df.loc[row, lim_min_col], param
        )
        param = np.where(
            param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param
        )

    elif df.loc[row, dist_col] == "Exponencial":
        param = expon.rvs(
            loc=df.loc[row, loc_col],
            scale=df.loc[row, scale_col],
            size=iter,
            random_state=rng,
        )
        param = np.where(
            param > df.loc[row, lim_max_col],
            df.loc[row, lim_max_col],
            param,
        )

    elif df.loc[row, dist_col] == "Rectangular":
        param = uniform.rvs(
            loc=df.loc[row, loc_col],
            scale=df.loc[row, scale_col],
            size=iter,
            random_state=rng,
        )

    return param
