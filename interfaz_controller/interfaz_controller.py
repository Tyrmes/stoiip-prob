import numpy as np
import xlwings as xw


def main(workbook: xw.Book = None):
    wb = xw.Book.caller()
    sheet = wb.sheets[0]

    # Cells B4 to B8 are called with the name Ranges, defined on the name manager from Ms Excel
    params = sheet['Ranges'].options(np.array, transpose=True).value
    sheet['stoiip'].value = 7758 * params[0] * params[1] * params[2] * (1 - params[3]) / params[4]


if __name__ == "__main__":
    xw.Book("interfaz_controller.xlsm").set_mock_caller()
    main()



