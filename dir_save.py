import os

def save_uploaded_file(directory, file):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(os.path.join(directory, file.name), 'wb') as f:
        f.write(file.getbuffer())
        
        
def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)