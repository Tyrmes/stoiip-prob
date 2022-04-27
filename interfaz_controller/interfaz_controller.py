import numpy as np
import pandas as pd
import xlwings as xw
from scipy.stats import expon, lognorm, norm, triang, uniform


def param_stoiip(df, row, dist_col, loc_col, scale_col, sc_col, iter, lim_min_col=None, lim_max_col=None):

    if df.loc[row, dist_col] == 'Normal':
        param = norm.rvs(loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)
        param = np.where(param < df.loc[row, lim_min_col], df.loc[row, lim_min_col], param)
        param = np.where(param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param)

    elif df.loc[row, dist_col] == 'Log-Normal':
        param = lognorm.rvs(s=df.loc[row, sc_col], loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)
        param = np.where(param < df.loc[row, lim_min_col], df.loc[row, lim_min_col], param)
        param = np.where(param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param)

    elif df.loc[row, dist_col] == 'Exponencial':
        param = expon.rvs(loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)
        param = np.where(param > df.loc[row, lim_max_col], df.loc[row, lim_max_col], param)

    elif df.loc[row, dist_col] == 'Triangular':
        param = triang.rvs(c=df.loc[row, sc_col], loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)

    elif df.loc[row, dist_col] == 'Rectangular':
        param = uniform.rvs(loc=df.loc[row, loc_col], scale=df.loc[row, scale_col], size=iter)

    return param


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

    area = param_stoiip(df_stoiip, 0, 'Distribución', 'Loc', 'Scale', 'Sc', iterations, 'Límite min', 'Límite max')
    thickness = param_stoiip(df_stoiip, 1, 'Distribución', 'Loc', 'Scale', 'Sc', iterations, 'Límite min', 'Límite max')
    porosity = param_stoiip(df_stoiip, 2, 'Distribución', 'Loc', 'Scale', 'Sc', iterations, 'Límite min', 'Límite max')
    swc = param_stoiip(df_stoiip, 3, 'Distribución', 'Loc', 'Scale', 'Sc', iterations, 'Límite min', 'Límite max')
    boi = param_stoiip(df_stoiip, 4, 'Distribución', 'Loc', 'Scale', 'Sc', iterations, 'Límite min', 'Límite max')

    sheet['stoiip_prob'].value = (7758 * area * thickness * porosity * (1 - swc) / boi).mean()


if __name__ == "__main__":
    xw.Book("interfaz_controller.xlsm").set_mock_caller()
    main()



