import difflib

with open('text1','r') as file:
	t1 = file.readlines()

with open('text2','r') as file:
	t2 = file.readlines()

d = difflib.Differ()
print('\n'.join(d.compare(t1,t2)))
