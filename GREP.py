import subprocess
import os
from subprocess import Popen, PIPE
import time

#print(34)

Index=[]

def get_files(directory_path):
	file_paths=[]
	for root,dirs,files in os.walk(directory_path):
		for f in files:
			file_paths.append(os.path.join(root,f))
	return file_paths


def get_output(query_file,response):
	f=open(query_file,'r')
	f2=open('grep_output.txt','w')
	for sent in f:
		dist=[]
		sent=sent.strip()
		words=sent.split(" ")
		index=words[0]
		words=words[1:]
		#response=Response
		for wrd in words:
			#dist=[]
			process=Popen(["grep",'-lr',wrd,'alldocs/'],stdout=PIPE)
			s=str(process.stdout.read())
			s=s.replace("'",'')
			temp=s.split("\\n")
			#print(temp)
			dist.append(set(temp))
		print(index)
		Index.append(index)
		try:
			f2.write(index)
			f2.write('\n')
			response[index]=set.intersection(*dist)
			for x in response[index]:
				f2.write(x)
				f2.write('\n')
			#print(response)
			#break
		except:
			pass
	f2.close()


#file_paths=get_files('E:/7th Sem/IR/Assignment 1/alldocs')
query_file='E:/7th Sem/IR/Assignment 1/query.txt'
response={}
t0=time.time()
get_output(query_file,response)
t1=time.time()
time_taken=t1-t0
f=open('grep_out.txt','w')
f.write('time_taken=')
f.write(str(time_taken))
f.write('\n')
f.close()
