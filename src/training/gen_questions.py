import sys, os
import subprocess

dirs = ['../tests/music_instruments/']#, '['../tests/cities/', '../tests/constellations/', '../tests/languages/', '../tests/music_instruments/']

paths = []

for path in dirs:
	paths.append([os.path.join(path,fn) for fn in next(os.walk(path))[2]])
#end for

f = open('output.txt', 'w')

for path in paths:
	for fpath in path:
		cmd = ['python', 'ask.py', str(fpath), '1']
		subprocess.call(cmd, stdout=f)
	#end for
#end for