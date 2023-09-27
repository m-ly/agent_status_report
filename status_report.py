import pandas as pd
import xlrd
import os

POSITIONS = ['channel_1', 'channel_2', 'fire', 'phones', 'ch1', 'ch2']
fire_input = "2023-09-24_0908-fire.xls"
ch1_input =  "2023-09-24_0908-ch1.xls"

def set_working_dataframe(filename):
  wb = xlrd.open_workbook(filename, logfile=open(os.devnull, 'w'))
  return pd.read_excel(wb)

fire_data = set_working_dataframe(fire_input)
ch1_data = set_working_dataframe(ch1_input)

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

filtered_data = current_working_data(fire_data)
ch1_data = current_working_data(ch1_data)

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


fire_data = agent_time_df(fire_input,filtered_data)
fire_data_2 = agent_time_df(fire_input,filtered_data)
ch1_data = agent_time_df(ch1_input, ch1_data)

frames = [fire_data, fire_data_2, ch1_data]

# df = pd.merge(filtered_data, ch1_data, on='Agents')
df = pd.concat(frames, axis=1)
df = df.groupby(df.columns, axis=1).sum()
print(df)

#filtered_data.to_csv("monthly_status_report.xlsx")
  