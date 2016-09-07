import os
import nltk
import time

def get_files(directory_path):
	file_paths={}
	count=1
	for root,dirs,files in os.walk(directory_path):
		for f in files:
			file_paths[count]=os.path.join(root,f)
			count+=1
	return file_paths

class indexing:
	file_paths={}
	term_dict={}
	Lemmatizer=nltk.WordNetLemmatizer()
	#Train_text=nltk.corpus.state_union.raw('E:/7th Sem/IR/Assignment 1/Solution/Train.txt')
	#customized_sen_tokenizer=nltk.tokenize.PunktSentenceTokenizer(Train_text)
	stop_words={'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}
	stop_words.update([',','.',';',':','-','"',"'",'?','/',"\\",'=','!','$','#','*','(',')','{','}','[',']'])
	def _init_(self,directory_path):
		self.file_paths=get_files(directory_path)

	def get_wordnet_pos(self,treebank_tag):
		if treebank_tag.startswith('J'):
			return nltk.corpus.wordnet.ADJ
		if treebank_tag.startswith('V'):
			return nltk.corpus.wordnet.VERB
		if treebank_tag.startswith('N'):
			return nltk.corpus.wordnet.NOUN
		if treebank_tag.startswith('R'):
			return nltk.corpus.wordnet.ADV
		else:
			return nltk.corpus.wordnet.NOUN

	def tokenize(self):
		for i in range(len(self.file_paths)):
			print(i+1)
			f=open(self.file_paths[i+1],'rb')
			Dict={}
			s=str(f.read())
			#try:
			#s=str(f.read())
			s=s.lower()
			s=s.replace("\\r",' ')
			s=s.replace("\\n",' ')
			s=s.replace("\\",'')
			s=s.replace('=',' ')
			s=s.replace("'",' ')
			s=s.replace(',',' ')
			s=s.replace(':',' ')
			s=s.replace('|','')
			Tokenized=nltk.sent_tokenize(s)
			for sent in Tokenized:
				word=nltk.word_tokenize(sent)
				words=nltk.pos_tag(word)
				#print(words)
				for wrd,val in words:
					if wrd not in self.stop_words:
						val=self.get_wordnet_pos(val)
						#try:
						lem_wrd=self.Lemmatizer.lemmatize(wrd,val)
						if lem_wrd not in self.term_dict:
							self.term_dict[lem_wrd]=[]
							self.term_dict[lem_wrd].append(i+1)
						if i+1 not in self.term_dict[lem_wrd]:
							self.term_dict[lem_wrd].append(i+1)
						#except:
							#pass
							#print(val)
		#print(self.term_dict)
			#except:
				#pass
	def List_merge(self,list1,list2):
		list_merge=[]
		if(len(list1)<len(list2)):
			for i in list1:
				if i in list2:
					list_merge.append(i)
		else:
			for i in list2:
				if i in list1:
					list_merge.append(i)
		return list_merge

	def query_process(self,query):
		#f=open(file,'rb')
		total_result_list=[]
		#s=str(f.read())
		#try:
		#s=str(f.read())
		s=query
		s=s.lower()
		s=s.replace("\\r",' ')
		s=s.replace("\\n",' ')
		s=s.replace("\\",'')
		s=s.replace('=',' ')
		s=s.replace("'",' ')
		s=s.replace(',',' ')
		s=s.replace(':',' ')
		s=s.replace('|','')
		#Tokenized=nltk.sent_tokenize(s)
		#for sent in Tokenized:
		Dict=[]
		result_list=[]
		word=nltk.word_tokenize(s)
		#word=word[1:]
		words=nltk.pos_tag(word)
			#print(words)
		for wrd,val in words:
			if wrd not in self.stop_words:
				val=self.get_wordnet_pos(val)
				#try:
				lem_wrd=self.Lemmatizer.lemmatize(wrd,val)
				Dict.append(lem_wrd)
		result_list=self.term_dict[Dict[0]]
		for i in range(len(Dict)-1):
			try:
				result_list=self.List_merge(result_list,self.term_dict[Dict[i+1]])
			except:
				pass
		#total_result_list.append(result_list)
		return result_list

	def query_out_put(self,query):
		result_list=self.query_process(query)
		out=[]
		for x in result_list:
			out.append(self.file_paths[x])
			#Query.append(out)
		return out




index=indexing()
index._init_('E:/7th Sem/IR/Assignment 1/alldocs')
index.tokenize()
t2=0.0
f=open('E:/7th Sem/IR/Assignment 1/query.txt','r')
f1=open('Index_output.txt','w')
try:
	for line in f:
		print(line)
		line=line.strip()
		words=line.split()
		_id=words[0]
		words=words[1:]
		line=''
		for x in words:
			line=line+" "+x
		#print(line)
		t0=time.time()
		dist=index.query_out_put(line)
		t1=time.time()
		t2=t2+(t1-t0)
		f1.write('\n')
		f1.write(str(_id))
		f1.write('\n')
		for x in dist:
			f1.write(str(x))
			f1.write('\n')
		f1.write('\n')
except:
	pass
f1.write('time taken=')
f1.write(str(t2))
f1.close()
f.close()

#