import numpy as np
import pandas as pd
import xlwings as xw
from scipy.stats import expon, lognorm, norm, triang, uniform


def param_stoiip(df, row, dist_col, loc_col, scale_col, iter, sc_col=None, lim_min_col=None, lim_max_col=None):

    if df.loc[row, dist_col] == 'Log-Normal' or df.loc[row, dist_col] == 'Triangular':
        if df.loc[row, dist_col] == 'Log-Normal':
            param = lognorm.rvs(s=df.loc[row, sc_col], loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)
            param = np.where(param < df.loc[row, lim_min_col], df.loc[row, lim_min_col], param)
            param = np.where(param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param)

        elif df.loc[row, dist_col] == 'Triangular':
            param = triang.rvs(c=df.loc[row, sc_col], loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)

    elif df.loc[row, dist_col] == 'Normal':
        param = norm.rvs(loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)
        param = np.where(param < df.loc[row, lim_min_col], df.loc[row, lim_min_col], param)
        param = np.where(param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param)

    elif df.loc[row, dist_col] == 'Exponencial':
        param = expon.rvs(loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)
        param = np.where(param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param)

    elif df.loc[row, dist_col] == 'Rectangular':
        param = uniform.rvs(loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)

    return param

# Name of columns


dist = 'Distribución'
loc = 'Loc'
scale = 'Scale'
sc = 'Sc'
Lim_min = 'Límite min'
Lim_max = 'Límite max'


def main(workbook: xw.Book = None):
    wb = xw.Book.caller()
    sheet = wb.sheets[0]

    # Deterministic Stoiip
    # Cells B4 to B8 are called with the name Ranges, defined on the name manager from Ms Excel
    params = sheet['Ranges'].options(np.array, transpose=True).value
    sheet['stoiip'].value = 7758 * params[0] * params[1] * params[2] * (1 - params[3]) / params[4]

    # Stochastic Stoiip
    df_stoiip = sheet['df_stoiip'].options(pd.DataFrame, index=False, expand='table').value
    iterations = sheet['iterations'].value

    area = param_stoiip(df_stoiip, 0, dist, loc, scale, iterations, sc, Lim_min, Lim_max)
    thickness = param_stoiip(df_stoiip, 1, dist, loc, scale, iterations, sc, Lim_min, Lim_max)
    porosity = param_stoiip(df_stoiip, 2, dist, loc, scale, iterations, sc, Lim_min, Lim_max)
    swc = param_stoiip(df_stoiip, 3, dist, loc, scale, iterations, sc, Lim_min, Lim_max)
    boi = param_stoiip(df_stoiip, 4, dist, loc, scale, iterations, sc, Lim_min, Lim_max)

    sheet['stoiip_prob'].value = (7758 * area * thickness * porosity * (1 - swc) / boi).mean()
    sheet['Std_stoiip'].value = (7758 * area * thickness * porosity * (1 - swc) / boi).std()
    sheet['p10_stoiip'].value = np.percentile((7758 * area * thickness * porosity * (1 - swc) / boi), 10)
    sheet['p50_stoiip'].value = np.percentile((7758 * area * thickness * porosity * (1 - swc) / boi), 50)
    sheet['p90_stoiip'].value = np.percentile((7758 * area * thickness * porosity * (1 - swc) / boi), 90)

    sheet_1 = wb.sheets[1]
    sheet_1['stoiip_array'].value = 7758 * area * thickness * porosity * (1 - swc) / boi


if __name__ == "__main__":
    xw.Book("interfaz_controller.xlsm").set_mock_caller()
    main()



