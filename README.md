IScript
=======

IScript is a prefix expression interpreter.<br />
<br />
IScript's example:<br />
&nbsp;&nbsp;(print (* (+ 1 2) 3) "\n")<br />
<br />
C Language's example:<br />
&nbsp;&nbsp;printf("%d\n", (1 + 2) * 3);<br />
<br />
How to execute IScript's code?<br />
&nbsp;&nbsp;python iscript.py SCIPRT_FILE<br />
&nbsp;&nbsp;or<br />
&nbsp;&nbsp;./iscript.py SCRIPT_FILE<br />
<br />
core.py is interpreter core.<br />
funcs.py is including function definition. function 'print' is defined in funcs.py.<br />
iscript.py is calling core.py and funcs.py.<br />
sexp.iscript is a prefix expression calculator that is implemented by IScript.<br />

