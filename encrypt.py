from cryptography.fernet import Fernet
from os.path import join
from os import mkdir

with open('key.key', 'rb') as key_file:
  key = key_file.read()
  key_file.close()

fernet = Fernet(key)

alphabet = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
rot = 17

if input("Is the target a file (Y/n): ").lower() in ("n", "no"):
  # Directory encryption
  from os import listdir, getcwd, chdir, remove
  from os.path import isfile
  from shutil import rmtree
  from zipfile import ZipFile
  dir = join(getcwd(), input("Enter the directory path: "))
  
  files = [f for f in listdir(dir) if isfile(join(dir, f))]
  
  
  try:
    mkdir(join(dir, "encrypted"))
  except FileExistsError:
    pass

  chdir(join(dir, "encrypted"))

  for file in files:
    with open(join(dir, file), 'rb') as f:
      data = f.read()
      f.close()
    
    file_name = []
    
    # file name obfuscation
    for i in range(len(list(file))):
      index = alphabet.find(file[i])
      if index == -1:
        file_name.append(file[i])
      else:
        file_name.append(alphabet[index + rot])
        
    file_name = "".join(file_name)
    
    encrypted = fernet.encrypt(data)
    
    with open(join(dir, "encrypted", file_name), 'wb') as f:
      f.write(encrypted)
      f.close()
      
    with ZipFile(join(dir, "encrypted.zip"), 'a') as zip:
      zip.write(file_name)
      zip.close()
      
    remove(join(dir, file))

  chdir(dir)

  rmtree(join(dir, "encrypted"))

else:
  file = input("Enter the file path: ")
  
  try:
    mkdir(join("encrypted"))
  except FileExistsError:
    pass
  
  with open(join(file), 'rb') as f:
    data = f.read()
    
    file_name = []
    
    for i in range(len(list(file))):
      index = alphabet.find(file[i])
      if index == -1:
        file_name.append(file[i])
      else:
        file_name.append(alphabet[index + rot])
        
    file_name = "".join(file_name)
    encrypted = fernet.encrypt(data)
    with open(join("encrypted", file_name), 'wb') as f:
      f.write(encrypted)