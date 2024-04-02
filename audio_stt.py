import os
from os import path
import shutil
import time
import numpy as np

from tqdm import tqdm
import re
import pandas as pd
import librosa
import soundfile as sf
from pydub import AudioSegment
from openai import OpenAI

from dotenv import load_dotenv
from dir_save import make_dir

load_dotenv()
client = OpenAI()

def audio_wav():
    
    uploaded_path = './uploaded_back/'
    wav_path = './wav/'
    
    file_list = os.listdir(uploaded_path)
    make_dir(wav_path)
    wav_check = os.listdir(wav_path)
    
    file_list_py = [file for file in file_list if (file.endswith('.mp3') | file.endswith('.m4a') | file.endswith('.mp4'))]

    for file in file_list_py:
        m4a_file = uploaded_path+file
        name = file.split('.')[0]
        
        wav_filename = wav_path + name + '.wav'

        if file.split('.')[1].lower() =='m4a':
            sound = AudioSegment.from_file(m4a_file, format='m4a')
            sound.export(wav_filename, format='wav')
        elif file.split('.')[1].lower() =='mp3':
            sound = AudioSegment.from_file(m4a_file, format='mp3')
            sound.export(wav_filename, format='wav')
        elif file.split('.')[1].lower() =='mp4':
            sound = AudioSegment.from_file(m4a_file, format='mp4')
            sound.export(wav_filename, format='wav')
        
            
        song = AudioSegment.from_wav(wav_filename)
        song = song + 30
        song.export(wav_filename , 'wav')
    
    shutil.rmtree(uploaded_path)
    devide_file_path = './devide/'
    make_dir(devide_file_path)
    
    wav_path = './wav/'
    
    file_list = os.listdir(wav_path)
    
    for file in file_list:
        y, sr = librosa.load(wav_path + file, sr=16000)
        i=0
        start = 0
        end = 3000000
        
        while end < len(y):
            sf.write(devide_file_path + file[:-4] + f'_{i}' + '.wav', y[start:end], 16000, format='WAV', endian='LITTLE', subtype='PCM_16')
            start += 3000000
            end += 3000000
            i+=1
        
        sf.write(devide_file_path + file[:-4] + f'_{i}' + '.wav' , y[start:], 16000, format='WAV', endian='LITTLE', subtype='PCM_16')
    shutil.rmtree(wav_path)
    
def stt():
    audio_wav()
    devide_file_path = './devide/'
    wave_file_list = os.listdir(devide_file_path)
    text = {}
    
    ### srt 작업
    # for file in tqdm(wave_file_list):
    #     start = time.time()
    #     audio = open(devide_file_path+ file, 'rb')
        
    #     transcript = client.audio.transcriptions.create(
    #         model="whisper-1", 
    #         file= audio,
    #         response_format="srt",
    #     )
    #     text[file] = transcript
    #     end = time.time()
    #     second = f"{end - start:.1f} sec"
    #     print(file+second)
    #     audio.close()
    
    # text_str = ''
    
    # for k, v in text.items():
    #     temp = re.sub(r"[^가-힣\s.]", "", v)
    #     temp = temp.replace('\n\n', '',)
    #     text_str += temp
        
    # return text_str
    

    ### text 작업
    for file in tqdm(wave_file_list):
        start = time.time()
        audio = open(devide_file_path+ file, 'rb')
        
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file= audio,
        )
        text[file] = transcript.text
        end = time.time()
        second = f"{end - start:.1f} sec"
        print(file+second)
        audio.close()
    
    df = pd.DataFrame(columns=['hospital', 'num', 'text'])
    hospital_list = []
    num_list = []
    text_list = []
    
    for k, v in text.items():
        hospital_list.append(k.split('.')[0])
        num_list.append(k.split('.')[0].split('_')[-1])
        text_list.append(v)
    
    df = pd.DataFrame({"hospital":hospital_list,
                        "num":num_list,
                        "text":text_list,})
    
    df['hospital']=df["hospital"].str.extract('([a-zA-Z가-힣]+)')
    df['num']=df['num'].astype(int)
    df.sort_values(by= ['hospital', 'num'], ascending=[True,True], inplace=True)
    df.reset_index(inplace=True, drop=True)
    
    charting_dict = {}
    
    for h in tqdm(df['hospital'].unique()):
        charting_dict[h] = df[df['hospital'] == h]['text'].sum()
    
    print(charting_dict)
    
    shutil.rmtree(devide_file_path)
    
    return charting_dict

    