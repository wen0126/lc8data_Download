import wget,os
from subprocess import call

IDM = r'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'

file_path = './23031/gs23031_url.txt'
base_path = os.path.dirname(os.path.abspath(file_path))
with open(file_path,'r') as f:
    file = f.read()
file_list = eval(file)
for key in file_list.keys():
    entity_dir = os.path.join(base_path, key)
    os.makedirs(entity_dir, exist_ok=True)
    os.chdir(entity_dir)
    #print(os.getcwd())
    value = file_list[key]
    for url in value:
        name = url.split('/')[-1]
        if os.path.exists(name):
            print('\nDownloaded: ',name)
            continue
        print('\nDownloading: ',name)
        try:
            #wget.download(url)
            call([IDM,'/d',url,'/p',entity_dir,'/f',name,'/n','/a'])
        except:
            continue
