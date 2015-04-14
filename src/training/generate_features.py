input_file_name = 'output4.txt'
output_file_name = 'features4.txt'

in_file = open(input_file_name, 'r')
out_file = open(output_file_name,'w')

for line in in_file:
	features = line.split('|')[1:]

	f_len = len(features)
	ctr = 0
	for feature in features:
		if ctr != (f_len - 1):
			out_file.write(str(feature) + ',')
		else:
			out_file.write(str(feature))
		#end if
		ctr += 1
	#end for
#end for

in_file.close()
out_file.close()