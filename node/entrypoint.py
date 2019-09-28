import os
import subprocess

if os.environ['DEBUG'] == 'true':
    cmd = 'yarn && yarn run dev'
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
