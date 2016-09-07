import os
from datetime import datetime
from elasticsearch import Elasticsearch
import time

#ES_host={'host':'localhost','port':9200}

es = Elasticsearch('http://localhost:9200/',timeout=30,max_retries=10,retry_on_timeout=True)
request={
	"settings":{
	"number_of_shards":"1",
	"number_of_replicas":"0",
	"analysis": {
      "analyzer": {
        "full_name": {
          "filter": [
            "standard",
            "lowercase",
            "asciifolding"
          ],
            "type": "custom",
            "tokenizer": "standard"
        		}
      		}
    	}
	}
}

try:
	es.delete_index('doc')
except:
	pass
res=es.create(index='doc',doc_type='text',body=request)
print(res)


def get_files(directory_path):
	file_paths=[]
	#count=1
	for root,dirs,files in os.walk(directory_path):
		for f in files:
			file_paths.append(os.path.join(root,f))
	return file_paths

def indexing(file_paths):
	count=1
	for file in file_paths:
		f=open(file,'rb')
		s=str(f.read())
		res=es.create(index='doc',doc_type='text',body={'content':s,'name':file})
		print(count)
		print(res)
		count=count+1

def search(query_file_path,List,Dist):
	f=open(query_file_path,'r')
	#f2=open('Elastic_search_output.txt','w')
	for line in f:
		print(line)
		line=line.strip()
		words=line.split(" ")
		#print(words)
		index=words[0]
		try:
			query=words[2]
			line=words[3:]
		except:
			continue
		for x in words:
			query=query+" "+x
		print(query)
		res=es.search(index='doc',doc_type='text',body={"from":0,"size":300,"query":{"match":{"content":query}}})
		print(index)
		List.append(index)
		print(res['hits']['total'])
		#f2.write(str(index))
		#f2.write("\n")
		rest=[]
		for doc in res['hits']['hits']:
			#f2.write("%s" % (doc['_source']['name']))
			#f2.write("\n")
			if (doc['_source']['name']) not in rest:
				rest.append(doc['_source']['name'])
			if len(rest)>60:
				break
		Dist[index]=rest
		#f2.close()
	f.close()


file_paths=get_files('E:/7th Sem/IR/Assignment 1/alldocs')
indexing(file_paths)
t0=time.time()
List=[]
Dist={}
search('E:/7th Sem/IR/Assignment 1/query.txt',List,Dist)
t1=time.time()
f2=open('Elastic_search_output.txt','a')
f2.write(str(t1-t0))
f2.write('\n')
for x in List:
	f2.write(x)
	f2.write('\n')
	for z in Dist[x]:
		f2.write(z)
		f2.write('\n')
	f2.write('\n')
f2.close()
