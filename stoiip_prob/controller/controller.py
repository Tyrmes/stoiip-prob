import numpy as np
import pandas as pd
import xlwings as xw
from stoiip_prob.model.stoiip import stoiip
from stoiip_prob.model.utils import param_stoiip
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker

# Sheets' name
SHT_SUMMARY = "Resumen"
SHT_RESULTS = "Resultados"
# Name of columns for distribution definitions
INPUT_VAR_NAMES = "Variables"
DIST = "Distribución"
LOC = "Loc"
SCALE = "Scale"
SC = "Sc"
LIM_MIN = "Límite min"
LIM_MAX = "Límite max"
# Row indexes for dataframe with stochastic values from excel file
AREA_IDX, H_IDX, PORO_IDX, SW_IDX, BOI_IDX = 0, 1, 2, 3, 4
# Named ranges inside excel sheet to read values
DET_VALUES = "det_values"
STOC_VALUES = "df_stoiip"
ITERATIONS = "iterations"
SEED = "Seed"
# Named ranges inside excel sheet to write values
DET_STOIIP_CALC = "stoiip"
STOC_STOIIP_RESULTS = "stoiip_prob"
STOC_STOIIP_ARR = "stoiip_array"
# Indexes of summary results
P90_SUMM_IDX, P50_SUMM_IDX, P10_SUMM_IDX = 2, 3, 4
# Predefined percentile values
P10 = 90
P50 = 50
P90 = 10


def main(workbook: xw.Book = None):
    """
    This function connect Python with Ms. Excel trough xlwings in order to use the
    interface of this microsoft software as front-end to deploy results of deterministic
    and stochastic Stoiip.
    """
    wb = xw.Book.caller()
    sheet = wb.sheets[SHT_SUMMARY]

    # Deterministic Stoiip
    # Cells B4 to B8 are called with the name Ranges, defined on the name manager from
    # Ms. Excel
    params = sheet[DET_VALUES].options(np.array, transpose=True).value
    sheet[DET_STOIIP_CALC].value = stoiip(*params)

    # Stochastic Stoiip
    # Import dataframe from Ms. Excel
    df_stoiip = (
        sheet[STOC_VALUES].options(pd.DataFrame, index=False, expand="table").value
    )
    # Define Excel cell number of iterations
    iterations = int(sheet[ITERATIONS].value)

    # Define seed
    seed = int(sheet[SEED].value)

    # Define random values for stoiip variables
    input_col_names = df_stoiip[INPUT_VAR_NAMES].to_list()
    area_col, h_col, poro_col, sw_col, boi_col = tuple(input_col_names)
    input_idx = [AREA_IDX, H_IDX, PORO_IDX, SW_IDX, BOI_IDX]
    input_dict = dict(zip(input_col_names, input_idx))
    results_dict = {}

    for col, idx in input_dict.items():
        results_dict[col] = param_stoiip(
            df_stoiip, idx, DIST, LOC, SCALE, iterations, SC, LIM_MIN, LIM_MAX, seed
        )

    # Calculation of stoiip's mean, std, P10, P50, and P90
    results_dict[STOC_STOIIP_RESULTS] = stoiip(
        results_dict[area_col],
        results_dict[h_col],
        results_dict[poro_col],
        results_dict[sw_col],
        results_dict[boi_col],
    )

    stoiip_summary_results = [
        results_dict[STOC_STOIIP_RESULTS].mean(),
        results_dict[STOC_STOIIP_RESULTS].std(),
        np.percentile(results_dict[STOC_STOIIP_RESULTS], P90),
        np.percentile(results_dict[STOC_STOIIP_RESULTS], P50),
        np.percentile(results_dict[STOC_STOIIP_RESULTS], P10),
    ]
    sheet[STOC_STOIIP_RESULTS].options(transpose=True).value = stoiip_summary_results

    # Call second worksheet from workbook
    sheet_1 = wb.sheets[SHT_RESULTS]
    # Create results dataframe
    df_results = pd.DataFrame(results_dict)

    # Call stoiip's random values inside results worksheet
    sheet_1[STOC_STOIIP_ARR].options(index=False).value = df_results

    # Create histogram based on stoiip array
    eng_formatter = ticker.EngFormatter()
    sns.set_style("white")
    fig = plt.figure(figsize=(8, 6))
    ax = sns.histplot(df_results[STOC_STOIIP_RESULTS], color="lightgray", kde=True)
    plt.axvline(
        stoiip_summary_results[P90_SUMM_IDX],
        ymax=0.85,
        color="darkorange",
        linewidth=1.5,
        linestyle="--",
        label="P90",
    )
    plt.axvline(
        stoiip_summary_results[P50_SUMM_IDX],
        ymax=0.85,
        color="gold",
        linewidth=1.5,
        linestyle="--",
        label="P50",
    )
    plt.axvline(
        stoiip_summary_results[P10_SUMM_IDX],
        ymax=0.85,
        color="limegreen",
        linewidth=1.5,
        linestyle="--",
        label="P10",
    )
    ax.xaxis.set_major_formatter(eng_formatter)
    plt.xlabel("STOIIP (STB)")
    plt.suptitle("STOIIP Probabilístico")
    plt.legend(loc=0)
    plt.show()

    # Adding the plot to excel
    plot = sheet.pictures.add(
        fig, name="Histograma", update=True, left=sheet.range("J1").left
    )


if __name__ == "__main__":
    xw.Book("poes_excel.xlsm").set_mock_caller()
    main()
