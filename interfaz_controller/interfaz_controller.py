import numpy as np
import pandas as pd
import xlwings as xw
from scipy.stats import expon, lognorm, norm, triang, uniform


def sto_stoiip(dist, loc, scale, sc, iter, lim_min=None, lim_max=None):

    if dist == 'Normal':
        param = norm.rvs(loc=loc, scale=scale, size=iter)
        param = np.where(param < lim_min, lim_min, param)
        param = np.where(param > lim_max, lim_max, param)

    elif dist == 'Log-Normal':
        param = lognorm.rvs(s=sc, loc=loc, scale=scale, size=iter)
        param = np.where(param < lim_min, lim_min, param)
        param = np.where(param > lim_max, lim_max, param)

    elif dist == 'Exponencial':
        param = expon.rvs(loc=loc, scale=scale, size=iter)
        param = np.where(param > lim_max, lim_max, param)

    elif dist == 'Triangular':
        param = triang.rvs(c=sc, loc=loc, scale=scale, size=iter)

    elif dist == 'Rectangular':
        param = uniform.rvs(loc=loc, scale=scale, size=iter)

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

    area = sto_stoiip(, loc, scale, sc, iterations, lim_min, lim_max)
    thickness = sto_stoiip(dist, loc, scale, iterations, lim_min, lim_max)
    porosity = sto_stoiip(dist, loc, scale, iterations, lim_min, lim_max)
    swc = sto_stoiip(dist, loc, scale, iterations, lim_min, lim_max)
    boi = sto_stoiip(dist, loc, scale, iterations, lim_min, lim_max)

    sheet['stoiip_prob'].value = (7758 * area * thickness * porosity * (1 - swc) / boi).mean()

if __name__ == "__main__":
    xw.Book("interfaz_controller.xlsm").set_mock_caller()
    main()



