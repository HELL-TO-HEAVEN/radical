
import sys
from os import rename
from glob import glob

extension = sys.argv[1]		#for example .jpg/.tif/.BMP
name = '*' + extension 
i = 0

for fname in glob(name):
    rename(fname, 'file_'+str(i)+extension)
    i += 1
