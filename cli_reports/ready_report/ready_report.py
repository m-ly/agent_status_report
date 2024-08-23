import pandas as pd
import xlrd
import os
import sys


FILE = sys.argv[1]

def set_working_file(filename):
  wb = xlrd.open_workbook(filename, logfile=open(os.devnull, 'w'))
  data = pd.read_excel(wb)
  wb.release_resources()
  del wb
  return data

# input -> a string, a dataframe # output -> integer
def column_index(search_value, frame):
  for column in frame.columns:
    if (frame[column] == search_value).any():
      return frame.columns.get_loc(column)

def row_index(search_value, frame):
  for column in frame.columns:
    if (frame[column] == search_value).any():
      index = frame.loc[frame[column] == search_value].index[0]
      return index
      
def create_iter_range(start_row, end_row):
  result = []
  for index in range(start_row, end_row, 2):
    result.append(index)
  return result

def current_working_data(frame):
  user_col_index = column_index('Agent', frame)
  ready_col_index = column_index('Ready', frame)
  not_ready_col_index = column_index('Not Ready Total', frame)
  total_col_index = column_index('Logged On', frame)

  start_row = row_index('Agent', frame) + 2
  end_row = row_index('Overall:', frame) - 1

  filters = [user_col_index, ready_col_index, not_ready_col_index, total_col_index ]
  rows_range = create_iter_range(start_row, end_row)

  return frame.iloc[rows_range, filters]


# input -> string, output -> float : converts a string represting a number into decimal of hours
def format_time(number_string):
  numbers = number_string.split(':')
  numbers = [int(i) for i in numbers]
  if len(numbers) == 4:
    return round(((( numbers[0] * 24 + numbers[1] ) * 60 ) + numbers[2] ) / 60, 2)
  
  return round((numbers[0] * 60 + numbers[1]) / 60, 1)

# filter abomination of input table to return the columns 'ready''Not Ready Total'
def format_frame(df):
  df.rename(columns={df.columns[0]: 'Agents'}, inplace=True)
  df.rename(columns={df.columns[1]: 'Ready'}, inplace=True)
  df.rename(columns={df.columns[2]: 'UnReady'}, inplace=True)
  df.rename(columns={df.columns[3]: 'Total'}, inplace=True)

  df.iloc[:, 1:] = df.iloc[:, 1:].map(format_time)


# input -> xls file, output -> data frame
def create_frame(file):
      input_data = set_working_file(file)
      filtered_data = current_working_data(input_data)
      format_frame(filtered_data)
      return filtered_data


# input -> xls file, output -> xlsx file.
def report_writer(file):
  data = create_frame(file)

  # Insert new column tracking percentage between hours 
  for i in range(data.shape[1] - 1, 1, -1):
        col_name = f"{data.columns[i - 1]} %"
        data.insert(i, col_name, data.iloc[:, i - 1] / data.iloc[:, -1] * 100)



  data.to_excel(f"ready_report.xlsx", index=False)

report_writer(FILE)