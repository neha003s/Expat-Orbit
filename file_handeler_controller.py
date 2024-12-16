import pandas as pd
import os
import csv
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup


app = FastAPI()

folder_path = '/mnt/d/data_excel/2024'

#@app.get("/getallfiles")
@app.get("/")
#only "/" will provide the same result as getallfiles api.
def list_files():
    dir_list = os.listdir(folder_path)
    return dir_list

@app.get("/getfiledata/{fileName}")
def getFiledata(fileName: str):
    try:
        read_file = pd.read_excel(os.path.join(folder_path, fileName))
        new_path = os.path.join(folder_path, "csv")
        #folder_path+"/"+"csv/"
        if not os.path.exists(new_path):
            os.makedirs(new_path)

        csv_file_path = os.path.join(new_path, "temp.csv")
        read_file.to_csv(csv_file_path, index=None, header=None)

        # read_file.to_csv(new_path+"/temp.csv", index=None, header=None)
        df = pd.read_csv(csv_file_path)  # df = pd.read_csv(new_path+"/temp.csv")
        modifiedDF = df.dropna()
        modifiedDF.to_csv(csv_file_path, index=None, header=None)
        print(new_path)
        data_dict = make_json(csv_file_path)

        return JSONResponse(content=data_dict)
    except FileNotFoundError:
        return {"error": "File not found."}
    except Exception as e:
        return {"error": str(e)}
    # return json.dumps(data_dict, indent=4)


def make_json(csvFilePath):
    is_header = True
    headers = []
    data = []
    data_obj = {}
    addData = True
    with open(csvFilePath, encoding='utf-8') as csvf:
        reader = csv.reader(csvf)
        for row in reader:
            if is_header:
                headers = row
                is_header = False
                continue
            for i in range(len(headers)):
                if i == 0:
                    addData = True
                    data_obj = {}
                if headers[i].strip() == 'Company Type':
                    if row[i] != 'subsidiary of company incorporated outside India':
                        addData = False
                data_obj[headers[i].strip()] = row[i]
            if addData:
                data.append(data_obj)
    return data

