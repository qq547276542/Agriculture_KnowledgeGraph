with open('/home/kuangjun/predict_labels6.txt','r') as f:
	with open('/home/kuangjun/predict_labels7.txt','w') as fw:
		flag = 0 
		for line in f:
			#print(line)
			if(flag == 1):
				fw.write(line)

			if(line[0] == "=" and line[1] == "="):
				flag = 1
				print("ok")
