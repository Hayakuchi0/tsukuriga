import os
import subprocess

if os.environ['DEBUG'] == 'true':
    cmd = 'yarn && yarn run dev'
else:
    cmd = 'yarn && yarn run build'

p = subprocess.Popen(cmd, shell=True)
p.wait()
