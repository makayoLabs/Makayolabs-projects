import pandas as pd
import xlsxwriter

# Threshold data (you can later extend this with external files)
threshold_data = {
    2023: {"threshold": 81415, "rate": 0.15},
    2024: {"threshold": 91000, "rate": 0.15},
    2025: {"threshold": 95000, "rate": 0.15},
}

# Create workbook and add worksheets
workbook = xlsxwriter.Workbook("OAS_Recovery_Tax_Calculator.xlsx")
inputs_sheet = workbook.add_worksheet("Inputs & Results")
scenarios_sheet = workbook.add_worksheet("Scenarios")
guidance_sheet = workbook.add_worksheet("Guidance")
reports_sheet = workbook.add_worksheet("Reports")

# Formatting
header_format = workbook.add_format({'bold': True, 'bg_color': '#4F81BD', 'font_color': 'white', 'align': 'center'})
cell_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
currency_format = workbook.add_format({'num_format': '$#,##0.00', 'align': 'center'})
bold_format = workbook.add_format({'bold': True, 'align': 'left'})

# Populate "Inputs & Results" sheet
inputs_sheet.merge_range('A1:D1', "Inputs & Results", header_format)
inputs = [
    ["Input Field", "Description", "Value", "Notes"],
    ["Year", "Select year for calculation", 2024, "Dropdown"],
    ["OAS Benefits", "Total OAS received ($)", 8500, ""],
    ["Net Income", "Net income (line 23600) ($)", 95000, ""],
    ["RRSP Contributions", "Planned RRSP contributions ($)", 5000, ""],
]
outputs = [
    ["Output Field", "Description", "Formula"],
    ["Excess Income Over Threshold", "Income subject to clawback", "=[C3-C2]"],
    ["Recovery Tax Amount", "Clawback based on net income", "=MIN(C3,(C4*C5))"],
    ["Net OAS After Clawback", "Net OAS retained after clawback", "=C2-C4"]
]

# Write Inputs
inputs_sheet.write_row(1, 0, inputs[0], header_format)
for i, row in enumerate(inputs[1:], start=2):
    inputs_sheet.write_row(i, 0, row, cell_format)

# Add year dropdown
year_dropdown_range = [str(year) for year in threshold_data.keys()]
inputs_sheet.data_validation('C2', {'validate': 'list', 'source': year_dropdown_range})

# Write Outputs
start_row = len(inputs) + 2
inputs_sheet.write(start_row, 0, "Outputs", header_format)
for i, row in enumerate(outputs, start=start_row + 1):
    inputs_sheet.write_row(i, 0, row, cell_format)

# Populate "Scenarios" sheet
scenarios_sheet.merge_range('A1:D1', "Scenario Simulation", header_format)
scenarios_sheet.write(1, 0, "Adjust RRSP Contributions, Spousal Splitting, or Delay OAS to minimize clawback.", bold_format)

# Scenario table headers
scenario_headers = ["Scenario", "Variable Adjusted", "Impact on Recovery Tax", "Net OAS Retained"]
scenarios_sheet.write_row(3, 0, scenario_headers, header_format)

# Guidance Sheet
guidance_sheet.merge_range('A1:C1', "Guidance", header_format)
guidance = [
    ["Topic", "Details"],
    ["Thresholds", "Clawback applies when income exceeds the threshold for the year. It is recovered at 15% of excess income."],
    ["Tips to Reduce Clawback", "1. Contribute to RRSPs. 2. Split income with a spouse. 3. Delay OAS payments to a later age (up to 70)."]
]
for i, row in enumerate(guidance, start=2):
    guidance_sheet.write_row(i, 0, row, cell_format)

# Reports Sheet
reports_sheet.merge_range('A1:C1', "Summary Report", header_format)
reports_sheet.write("A2", "This sheet will contain the summary of inputs, results, and actionable recommendations.", bold_format)

# Save Workbook
workbook.close()
print("Excel file 'OAS_Recovery_Tax_Calculator.xlsx' created successfully!")
