import streamlit as st
from dir_save import save_uploaded_file
import io
import requests
from audio_stt import stt
  
def main():
   # host_url = "http://52.79.170.120:8000"
   host_url = "http://127.0.0.1:8000"
   # file_url = f"{host_url}/uploaded_back"
   file_url = f"{host_url}/uploadfile/"
   conversion_url = f"{host_url}/conversion"
   response = None
   response_text  = None
   
   st.title("차트 만들기")

   uploaded_file = st.file_uploader('WAV 파일 업로드', type=['wav','m4a','mp3','mp4'])

   
   if uploaded_file is not None:
      response_text = requests.post(file_url, files={'file':uploaded_file})
   else:
      st.error('wav 파일을 넣어주세요', icon="🚨")
   
   if st.button('차팅 시작'):
      if uploaded_file is None:
         print('파일 없음')
      else:
         response = requests.get(conversion_url)
       
   tab1, tab2 = st.tabs(["차팅", " "])
   # tab1 = st.tabs(["차팅"])
   # with tab1:
   #    st.header("본문")
   #    if response_text is not None:
   #       st.write(response_text.text)
      

   with tab1:
      st.header("차트 본문")
      
      if response is not None:
         response_dict = response.json()
         value = response_dict.get("charting", None)
         value = value.replace('\n', '\t\n\n')
         st.write(value)

if __name__ == "__main__":
   main()