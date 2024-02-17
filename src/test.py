import subprocess
import os

local_appdata_path = os.environ['LOCALAPPDATA']
vs_code_path = os.path.join(local_appdata_path, "Programs", "Microsoft VS Code", "Code.exe")
dir_path = r'E:\Python\goVenv'
subprocess.Popen([vs_code_path, dir_path])
