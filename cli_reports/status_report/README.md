# agent_status_report

### USAGE

The Filename will need to include what position the the report is tracking
When running the script, the argument passed to the script is the absolute path of the folder where the reports are stored

## given a directory as an input

For each xls file in the the directory, create a frame, and push the frame to an array
transform each element in the array to desired formatting - rename column
merge the frames into a single frame
write the frame to excel

# example usage

python3 status_report.py /Users/matthewlyell/Downloads/100823_week_end
