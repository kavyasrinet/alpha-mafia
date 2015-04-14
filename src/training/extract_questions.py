input_file_name = 'output4.txt'
output_file_name = 'question4.txt'

in_file = open(input_file_name, 'r')
out_file = open(output_file_name,'w')

for line in in_file:
	out_file.write(line.split('|',1)[0] + '\n')
#end for

in_file.close()
out_file.close()