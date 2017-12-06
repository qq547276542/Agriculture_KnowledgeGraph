
def merge():
	s = set()
	for i in range(10):
		filename = 'table'+str(i)+".txt"
		file_object = open('table'+str(i)+".txt",'r').read()
		table = file_object.split()
		for c in table:
			s.add(c)
	print(len(s))
	file_object = open("merge_table3.txt",'w')
	file_text = ""
	for i in s:
		file_text += i + " "
	file_object.write(file_text)
	file_object.close()
	
merge()