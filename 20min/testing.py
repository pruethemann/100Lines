import re

txt = '[(pru9)]'
print(txt)
code_str = re.sub("a-z", "", txt)
print(code_str)