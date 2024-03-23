from cryptography.fernet import Fernet
from os.path import join
from os import mkdir

with open('key.key', 'rb') as key_file:
  key = key_file.read()

fernet = Fernet(key)

alphabet = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"[::-1]
rot = 17

if input("Is the target a file (Y/n): ").lower() in ("n", "no"):
  # Directory encryption
  from os import listdir, remove
  from os.path import isfile
  from shutil import rmtree
  from zipfile import ZipFile
  dir = input("Enter the directory path: ")
  enc_dir = join(dir, "encrypted")
  
  with ZipFile(join(dir, "encrypted.zip"), 'r') as zip:
      zip.extractall(enc_dir)
  
  files = [f for f in listdir(enc_dir) if isfile(join(enc_dir, f))]
  
  for file in files:
    with open(join(enc_dir, file), 'rb') as f:
      data = f.read()
    
    file_name = []
    
    for i in range(len(list(file))):
      index = alphabet.find(file[i])
      if index == -1:
        file_name.append(file[i])
      else:
        file_name.append(alphabet[index + rot])
        
    file_name = "".join(file_name)
    decrypted = fernet.decrypt(data)
    with open(join(dir, file_name), 'wb') as f:
      f.write(decrypted)
    
  remove(join(dir, "encrypted.zip"))
  rmtree(enc_dir)
    
else:
  file = input("Enter the file path: ")
  
  try:
    mkdir(join("decrypted"))
  except FileExistsError:
    pass
  
  with open(join("encrypted", file), 'rb') as f:
    data = f.read()
    
    file_name = []
    
    for i in range(len(list(file))):
      index = alphabet.find(file[i])
      if index == -1:
        file_name.append(file[i])
      else:
        file_name.append(alphabet[index + rot])
        
    file_name = "".join(file_name)
    decrypted = fernet.decrypt(data)
    with open(join("decrypted", file_name), 'wb') as f:
      f.write(decrypted)