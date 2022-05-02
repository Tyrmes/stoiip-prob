import numpy as np
import pandas as pd
import xlwings as xw
from scipy.stats import expon, lognorm, norm, triang, uniform


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

    Returns
    -------
    numpy array of the any Stoiip parameter

    """
    if df.loc[row, dist_col] == "Log-Normal" or df.loc[row, dist_col] == "Triangular":
        if df.loc[row, dist_col] == "Log-Normal":
            param = lognorm.rvs(
                s=df.loc[row, sc_col],
                loc=df.loc[row, loc_col],
                scale=df.loc[row, scale_col],
                size=iter,
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
            )

    elif df.loc[row, dist_col] == "Normal":
        param = norm.rvs(
            loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter
        )
        param = np.where(
            param < df.loc[row, lim_min_col], df.loc[row, lim_min_col], param
        )
        param = np.where(
            param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param
        )

    elif df.loc[row, dist_col] == "Exponencial":
        param = expon.rvs(
            loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter
        )
        param = np.where(
            param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param
        )

    elif df.loc[row, dist_col] == "Rectangular":
        param = uniform.rvs(
            loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter
        )

    return param


# Name of columns


dist = "Distribución"
loc = "Loc"
scale = "Scale"
sc = "Sc"
Lim_min = "Límite min"
Lim_max = "Límite max"


def main(workbook: xw.Book = None):
    """
    This function connect Python with Ms. Excel trough xlwings in order to use the
    interface of this microsoft software as front-end to deploy results of deterministic
    and stochastic Stoiip.
    """
    wb = xw.Book.caller()
    sheet = wb.sheets[0]

    # Deterministic Stoiip
    # Cells B4 to B8 are called with the name Ranges, defined on the name manager from
    # Ms. Excel
    params = sheet["Ranges"].options(np.array, transpose=True).value
    sheet["stoiip"].value = (
        7758 * params[0] * params[1] * params[2] * (1 - params[3]) / params[4]
    )

    # Stochastic Stoiip
    # Import dataframe from Ms. Excel
    df_stoiip = (
        sheet["df_stoiip"].options(pd.DataFrame, index=False, expand="table").value
    )
    # Define Excel cell number of iterations
    iterations = int(sheet["iterations"].value)

    # Define seed
    seed = int(sheet["Seed"].value)
    np.random.seed(seed)

    # Define random values for stoiip variables
    area = param_stoiip(
        df_stoiip, 0, dist, loc, scale, iterations, sc, Lim_min, Lim_max
    )
    thickness = param_stoiip(
        df_stoiip, 1, dist, loc, scale, iterations, sc, Lim_min, Lim_max
    )
    porosity = param_stoiip(
        df_stoiip, 2, dist, loc, scale, iterations, sc, Lim_min, Lim_max
    )
    swc = param_stoiip(df_stoiip, 3, dist, loc, scale, iterations, sc, Lim_min, Lim_max)
    boi = param_stoiip(df_stoiip, 4, dist, loc, scale, iterations, sc, Lim_min, Lim_max)

    # Calculation of stoiip's mean, std, P10, P50, and P90
    sheet["stoiip_prob"].value = (
        7758 * area * thickness * porosity * (1 - swc) / boi
    ).mean()
    sheet["Std_stoiip"].value = (
        7758 * area * thickness * porosity * (1 - swc) / boi
    ).std()
    sheet["p10_stoiip"].value = np.percentile(
        (7758 * area * thickness * porosity * (1 - swc) / boi), 10
    )
    sheet["p50_stoiip"].value = np.percentile(
        (7758 * area * thickness * porosity * (1 - swc) / boi), 50
    )
    sheet["p90_stoiip"].value = np.percentile(
        (7758 * area * thickness * porosity * (1 - swc) / boi), 90
    )

    # Call second worksheet from workbook
    sheet_1 = wb.sheets[1]
    # Call stoiip's random values inside results worksheet
    stoiip = 7758 * area * thickness * porosity * (1 - swc) / boi
    sheet_1["stoiip_array"].options(np.array, transpose=True).value = stoiip


if __name__ == "__main__":
    xw.Book("interfaz_controller.xlsm").set_mock_caller()
    main()
