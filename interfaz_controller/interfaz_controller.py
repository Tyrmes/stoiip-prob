import numpy as np
import xlwings as xw


def main(workbook: xw.Book = None):
    wb = xw.Book.caller()
    sheet = wb.sheets[0]

    sheet.range('B4:B8').name = 'values'
    params = sheet['values'].options(np.array, transpose=True).value
    sheet['B10'].value = 7758 * params[0] * params[1] * params[2] * (1 - params[3]) / params[4]


if __name__ == "__main__":
    xw.Book("interfaz_controller.xlsm").set_mock_caller()
    main()


