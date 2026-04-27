import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import pingouin as pg
from gspread.utils import rowcol_to_a1

def automate_research():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('cronalpha.json', scope)
    client = gspread.authorize(creds)

    ss = client.open("PilotResponses")
    raw_sheet = ss.get_worksheet(0) 
    dash_sheet = ss.get_worksheet(1) 

    #get data & avoid specific columns
    df = pd.DataFrame(raw_sheet.get_all_records())

    #detects string columns and convert to numeric if possible
    numeric_df = df.apply(pd.to_numeric, errors='coerce')

    #likert scale filter
    items = numeric_df.dropna(axis=1, how='all') #text columns dropped
    #items = df.drop(df.columns[[0, 1, 2, 10, 11, 12, 13]], axis=1) #manual drop of non-likert columns
    items = items.loc[:, (items.max() <= 6) & (items.min() >= 1)]
    
    #dynamic
    num_responses = len(items)
    num_questions = len(items.columns)


    question_labels = [f"Q{i+1}" for i in range(num_questions)]

    #positions
    total_col_index = num_questions + 2
    last_q_letter = rowcol_to_a1(1, num_questions + 1)[0] 
    total_col_letter = rowcol_to_a1(1, total_col_index)[0] 
    summary_col_letter = rowcol_to_a1(1, total_col_index + 2)[0] 

    last_row = num_responses + 1 
    var_row_index = last_row + 1

    #calculations
    alpha, ci = pg.cronbach_alpha(data=items)
    variances = items.var(ddof=1).values.tolist()
    sum_item_variances = sum(variances)
    total_scores_var = items.sum(axis=1).var(ddof=1)

    #reset dashboard
    dash_sheet.clear() 
    dash_sheet.resize(rows=1000, cols=total_col_index + 5) 

    #insert data to dashboard

    #headers
    headers = ["Resp No."] + question_labels + ["Total"]
    dash_sheet.update('A1', [headers])

    #respondents id & data
    resp_ids = [[i+1] for i in range(num_responses)]
    dash_sheet.update('A2', resp_ids)
    dash_sheet.update('B2', items.values.tolist())

    #total
    total_formulas = [[f"=SUM(B{i}:{last_q_letter}{i})"] for i in range(2, last_row + 1)]
    dash_sheet.update(f'{total_col_letter}2:{total_col_letter}{last_row}', total_formulas, value_input_option='USER_ENTERED')

    #variance sample row
    dash_sheet.update_acell(f'A{var_row_index}', 'var-sample')
    dash_sheet.update(f'B{var_row_index}', [variances])
    
    #total variance formula
    dash_sheet.update(f'{total_col_letter}{var_row_index}', [[f"=SUM(B{var_row_index}:{last_q_letter}{var_row_index})"]], value_input_option='USER_ENTERED')

    #summary
    summary_data = [
        ["No. of items =", num_questions],
        ["Sum of item variances =", sum_item_variances],
        ["Variance of total scores =", total_scores_var],
        ["Cronbach's Alpha =", alpha],
        ["Designed and Built by: Peter Paul C. Abangan"]
    ]
    dash_sheet.update(f'{summary_col_letter}2', summary_data)

    #follows the tag
    name_cell_start = f"{summary_col_letter}6"
    name_cell_end = f"{rowcol_to_a1(6, total_col_index + 6)}"

    #design&built
    dash_sheet.format(name_cell_start, {
        "backgroundColor": {"red": 0.0, "green": 0.5, "blue": 1.0},
        "textFormat": {
            "fontFamily": "Cairo",
            "foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0},
            "bold": True,
            "italic": True,
            "fontSize": 12
        },
        "horizontalAlignment": "LEFT"
    })


    dash_sheet.merge_cells(f"{name_cell_start}:{name_cell_end}")

    print(f"Success! Total is in Col {total_col_letter}. Alpha: {alpha:.3f}")
    
automate_research()