from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from os import path
import shutil

from dir_save import save_uploaded_file, make_dir
from charting import run_charting
from audio_stt import stt


app = FastAPI()


def init_folder():
    path_list = ['./uploaded_back/', './wav/', './devide/']
    for d_path in path_list:
        if path.exists(d_path):
            shutil.rmtree(d_path)


@app.post('/uploaded_back')
async def upload(uploaded_file: UploadFile = File(...)):
    print(uploaded_file)


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    init_folder()
    upload_path = './uploaded_back/'
    make_dir(upload_path)
    
    file_name = file.filename
    
    with open(upload_path+file_name, "wb") as f:
        f.write(file.file.read())


@app.get("/conversion")
async def transcribe_audio():
    try:
        ## text 사용     
        charting_dict = stt()
        
        conversation = list(charting_dict.values())[0]
        charting = run_charting(conversation)
        result_dict = {"charting": charting}
        
        return result_dict
            
    except Exception as e:
        print(e)
        text = f"음성인식에서 실패했습니다. {e}"
        
        
app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
    allow_credentials=True,
    allow_methods={"OPTIONS", "GET", "POST"},
    allow_headers={"*"}
)


app.mount("/static", StaticFiles(directory="./static"), name='static')