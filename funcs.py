import sys
import core

funcs = {}

class UserFunc(object):
	def __init__(self, fname, args_list, ip):
		self.fname = fname
		self.args_list = args_list
		self.ip = ip

def _check_args(fname, args_count, args, types):
	if len(args) < args_count:
		raise Exception("Function(%s) too few arguments!" % fname)
	elif len(args) > args_count:
		raise Exception("Function(%s) too many arguments!" % fname)
	for i in range(len(args)):
		if not isinstance(args[i], types[i]):
			raise Exception("Function(%s) argument(%d) type is error!" % (fname, i))

def _check_vargs(fname, args, t):
	for i in range(len(args)):
		if not isinstance(args[i], t):
			raise Exception("Function(%s) argument(%d) type is error!" % (fname, i))

def _check_args_mt(fname, args_count, args, types):
	if len(args) < args_count:
		raise Exception("Function(%s) too few arguments!" % fname)
	elif len(args) > args_count:
		raise Exception("Function(%s) too many arguments!" % fname)
	for i in range(len(args)):
		match_type = False
		for t in types[i]:
			if isinstance(args[i], t):
				match_type = True
				break
		if not match_type:
			raise Exception("Function(%s) argument(%d) type is error!" % (fname, i))

def func_add(args):
	_check_args("+", 2, args, (float, float))
	return args[0] + args[1]

def func_sub(args):
	_check_args("-", 2, args, (float, float))
	return args[0] - args[1]

def func_mul(args):
	_check_args("*", 2, args, (float, float))
	return args[0] * args[1]

def func_div(args):
	_check_args("/", 2, args, (float, float))
	return args[0] / args[1]

def func_pow(args):
	_check_args("^", 2, args, (float, float))
	return args[0] ** args[1]

def func_mod(args):
	_check_args("%", 2, args, (float, float))
	return args[0] % args[1]

def func_neq(args):
	_check_args_mt("!=", 2, args, ((float, str, unicode), (float, str, unicode)))
	return args[0] != args[1]

def func_eq(args):
	_check_args_mt("=", 2, args, ((float, str, unicode), (float, str, unicode)))
	return args[0] == args[1]

def func_gt(args):
	_check_args_mt(">", 2, args, ((float, str, unicode), (float, str, unicode)))
	return args[0] > args[1]

def func_lt(args):
	_check_args_mt("<", 2, args, ((float, str, unicode), (float, str, unicode)))
	return args[0] < args[1]

def func_ge(args):
	_check_args_mt(">=", 2, args, ((float, str, unicode), (float, str, unicode)))
	return args[0] >= args[1]

def func_le(args):
	_check_args_mt("<=", 2, args, ((float, str, unicode), (float, str, unicode)))
	return args[0] <= args[1]

def func_input(args):
	_check_args("input", 0, args, ())
	return str(input())

def func_print(args):
	for item in args:
		sys.stdout.write(unicode(item))
		sys.stdout.flush()
	return None

def func_sum(args):
	_check_vargs("sum", args, float)
	total = 0.0
	for item in args:
		total = total + float(item)
	return total

def func_run(args):
	_check_args("run", 1, args, (core.InsPtr,))
	return core.run(args[0].code, args[0].ip)[0]

def func_exec(args):
	_check_vargs("exec", args, core.InsPtr)
	r = 0.0
	for item in args:
		r = core.run(item.code, item.ip)[0]
	return r

def func_if(args):
	if len(args) == 2:
		_check_args("if", 2, args, (bool, core.InsPtr))
		if args[0]:
			return core.run(args[1].code, args[1].ip)[0]
	elif len(args) == 3:
		_check_args("if", 3, args, (bool, core.InsPtr, core.InsPtr))
		if args[0]:
			return core.run(args[1].code, args[1].ip)[0]
		else:
			return core.run(args[2].code, args[2].ip)[0]
	else:
		raise Exception("Invalid if")

def func_str(args):
	if(len(args) != 1):
		raise Exception("Invalid str")
	return str(args[0])

def func_float(args):
	if(len(args) != 1):
		raise Exception("Invalid float")
	return float(args[0])

def func_symbol(args):
	_check_args("symbol", 2, args, (core.InsPtr, float))
	return args[0].code[args[0].ip + int(args[1])]

def func_define(args):
	_check_args_mt("define", 2, args, ((core.Symbol,), (float, str, unicode)))
	core.define(args[0].symbol, args[1])
	return None

def func_set(args):
	_check_args_mt("set", 2, args, ((core.Symbol,), (float, str, unicode)))
	core.set_var(args[0].symbol, args[1])
	return None

def func_defun(args):
	if len(args) < 2 or not isinstance(args[0], core.Symbol):
		raise Exception("Expect function name")
	fname = args[0].symbol
	args_list = []
	i = 1
	while i < len(args):
		if isinstance(args[i], core.Symbol):
			args_list.append(args[i].symbol)
		else:
			break
		i = i + 1
	if i != len(args) - 1 or not isinstance(args[i], core.InsPtr):
		raise Exception("Invalid function definition")
	funcs[fname] = UserFunc(fname, args_list, args[i])
	return None

def func_v(args):
	_check_args_mt("v", 1, args, ((float, str, unicode, core.InsPtr),))
	return args[0]

def func_error(args):
	_check_args_mt("error", 1, args, ((str, unicode),))
	raise Exception(args[0])

def func_next(args):
	_check_args("next", 1, args, (core.InsPtr,))
	if args[0].ip + 1 >= len(args[0].code):
		raise Exception("Out of range")
	args[0].ip = args[0].ip + 1
	return args[0].code[args[0].ip - 1]

def func_prev(args):
	_check_args("prev", 1, args, (core.InsPtr,))
	if args[0].ip - 1 < 0:
		raise Exception("Out of range")
	args[0].ip = args[0].ip - 1
	return args[0].code[args[0].ip + 1]

def func_eos(args):
	_check_args("eos", 1, args, (core.InsPtr,))
	return args[0].ip >= len(args[0].code)

def init():
	funcs["+"] = func_add
	funcs["-"] = func_sub
	funcs["*"] = func_mul
	funcs["/"] = func_div
	funcs["^"] = func_pow
	funcs["%"] = func_mod
	funcs["!="] = func_neq
	funcs["="] = func_eq
	funcs[">"] = func_gt
	funcs["<"] = func_lt
	funcs[">="] = func_ge
	funcs["<="] = func_le
	funcs["input"] = func_input
	funcs["print"] = func_print
	funcs["sum"] = func_sum
	funcs["run"] = func_run
	funcs["exec"] = func_exec
	funcs["if"] = func_if
	funcs["str"] = func_str
	funcs["float"] = func_float
	funcs["symbol"] = func_symbol
	funcs["define"] = func_define
	funcs["set"] = func_set
	funcs["defun"] = func_defun
	funcs["v"] = func_v
	funcs["error"] = func_error
	funcs["next"] = func_next
	funcs["prev"] = func_prev
	funcs["eos"] = func_eos

def get_func(name):
	if name in funcs.keys():
		return funcs[name]
	else:
		return None
