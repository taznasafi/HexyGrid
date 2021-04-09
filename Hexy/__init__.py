import os
from sys import exit
# create initial Data folder for input and output
if not os.path.exists(r'./data'):
    os.mkdir(r'./data')

input_path = r'./data/input'
output_path = r'./data/output'
zipfolder_path = r'./data/input/extracted_zipfiles'
output_csv_path = r"./data/output/csv"
geo_json = r"./data/output/csv/geojson"
out_json = r"./data/output/csv/json"
input_json = r"./data/input/json"

if not os.path.exists(input_path):
    os.mkdir(input_path)
if not os.path.exists(output_path):
    os.mkdir(output_path)

if not os.path.exists(zipfolder_path):
    os.mkdir(zipfolder_path)

if not os.path.exists(output_csv_path):
    os.mkdir(output_csv_path)

if not os.path.exists(geo_json):
    os.mkdir(geo_json)

if not os.path.exists(out_json):
    os.mkdir(out_json)

if not os.path.exists(input_json):
    os.mkdir(input_json)

# if not os.path.exists('my_paths.py'):
#     print("PLEASE CREATE A PYTHON FILE CALLED: my_paths.py\n"
#           "create path object for:"
#           "\nXY_tests=''"
#           "\nblock_groups=''")
#     exit()