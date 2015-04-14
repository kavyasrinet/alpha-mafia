import requests

def coref_server_response(p_text):
	r = requests.post('http://localhost:8125/BARTDemo/ShowText/process/', data = p_text)

	if (r.status_code, r.reason) == (200, 'OK'):
		return r.text
	else:
		return None
	#end if
#end def

#unit test
if __name__ == '__main__':
	server_input = 'Bill is the president of the club. He lives in Pittsburgh.'

	print coref_server_response(server_input)
#end if