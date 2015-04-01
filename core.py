import funcs

class InsPtr(object):
	def __init__(self, code, ip):
		self.code = code
		self.ip = ip

class Symbol(object):
	def __init__(self, symbol):
		self.symbol = symbol

def lex(code):
	l = []
	buf = ""
	i = 0
	while i < len(code):
		char = code[i]
		if char == "(":
			if buf != "":
				l.append(buf)
				l.append("(")
				buf = ""
			else:
				l.append("(")
		elif char == ")":
			if buf != "":
				l.append(buf)
				l.append(")")
				buf = ""
			else:
				l.append(")")
		elif char == "\"":
			if buf != "":
				l.append(buf)
			buf = "\""
			i = i + 1
			while i < len(code):
				char = code[i]
				if(char == "\""):
					buf = buf + char
					l.append(buf)
					buf = ""
					break
				elif(char == "\\"):
					i = i + 1
					char = code[i]
					if char == "t":
						buf = buf + "\t"
					elif char == "r":
						buf = buf + "\r"
					elif char == "n":
						buf = buf + "\n"
					elif char == "\\":
						buf = buf + "\\"
				else:
					buf = buf + char
				i = i + 1
		elif char == " " or char == "\r" or char == "\n" or char == "\t":
			if buf != "":
				l.append(buf)
				buf = ""
		else:
			buf = buf + char
		i = i + 1
	return l

global vars_stack
vars_stack = []

def define(name, value):
	global vars_stack
	vars_stack[len(vars_stack) - 2][name] = value

def set_var(name, value):
	global vars_stack
	i = len(vars_stack) - 1
	while i >= 0:
		if name in vars_stack[i].keys():
			vars_stack[i][name] = value
			return
		i = i - 1
	raise Exception("Undifined var(%s)" % name)

def var_value(name):
	global vars_stack
	i = len(vars_stack) - 1
	while i >= 0:
		if name in vars_stack[i].keys():
			return vars_stack[i][name]
		i = i - 1
	raise Exception("Undifined var(%s)" % name)

def is_symbol(name):
	for c in name:
		if not ((c >= "a" and c <= "z") \
				or (c >= "A" and c <= "Z") \
				or (c >= "0" and c <= "9") \
				or c == "_"):
			return False
	return True

global current_code
global current_begin_ip
global current_end_ip
current_code = []
current_begin_ip = -1
current_end_ip = -1

def run(code, ip, call_arg_keys = [], call_args = []):
	global current_code
	global current_begin_ip
	global current_end_ip
	try:
		current_code = code;
		current_begin_ip = ip;
		if ip >= len(code) or code[ip] != "(":
			raise Exception("Expect (")
		global vars_stack
		vs = {"True":True, "False":False, "None":None}
		for i in range(0, len(call_arg_keys)):
			key = call_arg_keys[i]
			vs[key] = call_args[i]
		vars_stack.append(vs)
		ip = ip + 1
		if ip >= len(code):
			raise Exception("Expect function name")
		fname = code[ip]
		if fname == ")":
			raise Exception("Expect function name")
		ip = ip + 1
		args = []
		while code[ip] != ")":
			if code[ip] == "'":
				args.append(InsPtr(code, ip + 1))
				def skip(code, ip):
					if ip >= len(code) or code[ip] != "(":
						raise Exception("Expect (")
					ip = ip + 1
					if ip >= len(code):
						raise Exception("Expect )")
					while code[ip] != ")":
						if code[ip] == "(":
							ip = skip(code, ip) + 1
						else:
							ip = ip + 1
						if ip >= len(code):
							raise Exception("Expect )")
					return ip
				ip = skip(code, ip + 1)
			elif code[ip] == "(":
				result, ip = run(code, ip)
				args.append(result)
			else:
				value = code[ip]
				if value[0] == "\"":
					args.append(value[1:(len(value) - 1)])
				elif value.isdigit():
					args.append(float(value))
				elif value[0] == ",":
					args.append(Symbol(value[1:len(value)]))
				elif is_symbol(value):
					args.append(var_value(value))
				else:
					raise Exception("Invalid symbol(%s)" % value)
			ip = ip + 1
			if ip >= len(code):
				raise Exception("Expect )")
		r = 0.0
		func = funcs.get_func(fname)
		if func == None:
			raise Exception("Invalid function(%s)" % fname)
		elif isinstance(func, funcs.UserFunc):
			r, _ = run(func.ip.code, func.ip.ip, func.args_list, args)
		else:
			r = func(args)
		vars_stack.pop()
		return (r, ip)
	except Exception, e:
		current_end_ip = ip
		raise e

def init():
	funcs.init()
