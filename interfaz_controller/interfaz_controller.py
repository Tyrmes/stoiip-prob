import xlwings as xw


def main(workbook: xw.Book = None):
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    area = float(sheet['B4'].value)
    h = float(sheet['B5'].value)
    poro = float(sheet['B6'].value)
    sw = float(sheet['B7'].value)
    boi = float(sheet['B8'].value)
    sheet['B10'].value = 7758 * area * h * poro * (1 - sw) / boi


if __name__ == "__main__":
    xw.Book("interfaz_controller.xlsm").set_mock_caller()
    main()


