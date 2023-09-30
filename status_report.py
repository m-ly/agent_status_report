import pandas as pd
import xlrd
import os
import sys
import openpyxl


# given a directory as an input
    #For each xls file in the the directory, create a frame, and push the frame to an array
    # transform each element in the array to desired formatting - rename column
    # merge the frames into a single frame
    # write the frame to excel

directory = os.getcwd() + '/' + sys.argv[1]
POSITIONS = ['channel_1', 'channel_2', 'fire', 'phones', 'ch1', 'ch2']



def set_working_file(filename):
  wb = xlrd.open_workbook(filename, logfile=open(os.devnull, 'w'))
  return pd.read_excel(wb)


def set_position_name(filename, positions):
  for ele in positions:
    if ele.lower() in filename:
      return ele

def column_index(search_value, frame):
  for column in frame.columns:
    if (frame[column] == search_value).any():
      #print(frame.columns.get_loc(column))
      return frame.columns.get_loc(column)

def row_index(search_value, frame):
  for column in frame.columns:
    if (frame[column] == search_value).any():
      index = frame.loc[frame[column] == search_value].index[0]
      #print(f"Row Index: {index}")
      return index
      
def create_iter_range(start_row, end_row):
  result = []
  for index in range(start_row, end_row, 2):
    result.append(index)
  return result


def current_working_data(frame):
  user_column_index = column_index('Agent', frame)
  total_time_column_index = column_index('Logged On', frame)
  start_row = row_index('Agent', frame) + 2
  end_row = row_index('Overall:', frame) - 1
  #print(user_column_index, total_time_column_index, start_row, end_row)

  filters = [user_column_index, total_time_column_index]
  rows_range = create_iter_range(start_row, end_row)

  return frame.iloc[rows_range, filters]


def agent_time_df(filename, frame):
  agents = {}
  position = set_position_name(filename, POSITIONS).title()
  for _index,row in frame.iterrows():
    #agents[row.iloc[0].title()] = { position: format_time(row.iloc[1]) }
    agents[row.iloc[0].title()] = format_time(row.iloc[1])
  return pd.DataFrame({'Agents': list(agents.keys()), position: list(agents.values())})


def format_time(number_string):
  numbers = number_string.split(':')
  numbers = [int(i) for i in numbers]
  if len(numbers) == 4:
    return ((( numbers[0] * 24 + numbers[1] ) * 60 ) + numbers[1] ) / 60
  
  return round((numbers[0] * 60 + numbers[1]) / 60, 2)


def all_reports(directory):
  xls_files = [];
  for root_, dir_, files in os.walk(directory):
    for file in files:
      if file.endswith(".xls"):
        xls_files.append(directory + '/' + file)
  return xls_files

def create_frame(file):
      input_data = set_working_file(file)
      filtered_data = current_working_data(input_data)
      return  agent_time_df(file,filtered_data)


def copy_excel_template(date):
  wb = openpyxl.load_workbook('template.xlsx')
  ws = wb.create_sheet('data')
  for row in wb['sheet1'].rows:
    ws.append(row)
  wb.save(f"workbook_{date}_monthly_report.xlsx")

def report_writer(directory):
  reports = all_reports(directory)
  frames = []

  for file in reports:
    frames.append(create_frame(file))

  merged_frame = pd.concat(frames, axis=0)
  result = merged_frame.groupby('Agents').sum()
  result.reset_index(inplace=True)
  result.to_excel('monthly_status_report.xlsx', index=False)
  

report_writer(directory)
