import sys
import codecs
import core

def unescape(text):
	if text[0] != "\"":
		return text
	new_text = "\""
	for char in text[1:len(text) - 1]:
		if char == "\r":
			new_text = new_text + "\\r"
		elif char == "\n":
			new_text = new_text + "\\n"
		elif char == "\t":
			new_text = new_text + "\\t"
		elif char == "\v":
			new_text = new_text + "\\v"
		elif char == "\f":
			new_text = new_text + "\\f"
		else:
			new_text = new_text + char
	new_text = new_text + "\""
	return new_text

def main():
	if len(sys.argv) != 2:
		print "iscript {path}"
		return
	path = sys.argv[1]
	code = ""
	try:
		f = codecs.open(path, 'r', 'utf8')
		code = f.read()
		f.close()
	except:
		print "Cannot open ", path
		return
	core.init()
	try:
		core.run(core.lex(code), 0)
	except Exception, e:
		print "\nISCRIPT ERROR: ", 
		if core.current_begin_ip != -1:
			start = core.current_begin_ip
			end = core.current_end_ip
			for symbol in core.current_code[start:end]:
				print unescape(symbol),
			
		print "\n", e, "\n"

if __name__ == '__main__':
	main()
