IScript
=======

IScript is a prefix expression interpreter.

IScript's example:
    (print (* (+ 1 2) 3) "\n")

C Language's example:
    printf("%d\n", (1 + 2) * 3);

How to execute IScript's code?
    python iscript.py SCIPRT_FILE
    or
    ./iscript.py SCRIPT_FILE

core.py is interpreter core.
funcs.py is including function definition. function 'print' is defined in funcs.py.
iscript.py is calling core.py and funcs.py.
sexp.iscript is a prefix expression calculator that is implemented by IScript.

