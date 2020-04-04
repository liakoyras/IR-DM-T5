import os
import time
from collections import Counter
import nltk
from nltk.corpus import words
nltk.download('stopwords')
nltk.download('words')
nltk.download('wordnet')

##config-parameters##

query_file_name = 'IndriRunQuerry.queries.file.301-450-titles-descs.ERGASIA'
results = 'Evaluations/301-450-titles-descs-results.trec'
fbOrigWeight=0.1
use_stopwords=True

##-----------------##

def time_extraction(fun,args):
    start = time.time()
    fun(args)
    return time.time()-start

def ask_Y_N(question):
    answer = ' '
    answers = ['Y', 'y', 'N', 'n']
    while answer not in answers:
        answer = raw_input(question +' (y/n): ')
    return answer

def extract_la(lines):
    doc = []

    for i in lines:
        f = open('latimes/'+i[:-5].lower(), 'r')
        text = f.read().splitlines()
        for j in range(len(text)):
            if i in text[j]:
                p=j-1
                temp=[]
                while '</DOC>' not in text[p]:
                    temp.append(text[p])
                    p+=1
                temp.append('</DOC>')
                doc.append(temp)
                break

    return doc

            
def extract_ft(lines):
    doc = []

    f_text = []
    f_id = []
    f_text_id_low = []
    f_text_id_high = []
    
    for i in os.listdir('ft'):
        text = []
        text_id_low = []
        text_id_high = []
        for j in os.listdir('ft/'+i):    
            f = open('ft/'+i+'/'+j)
            temp = f.read().splitlines()
            pt = 0
            while '<DOCNO>' not in temp[pt]:
                pt+=1
            text_id_low.append(int(temp[pt].split('-')[1].split('<')[0]))
            pt = len(temp)-1
            while '<DOCNO>' not in temp[pt]:
                pt-=1
            text_id_high.append(int(temp[pt].split('-')[1].split('<')[0]))
            text.append(temp)
        f_text_id_low.append(text_id_low)
        f_text_id_high.append(text_id_high)
        f_text.append(text)
        f_id.append(i)  

    read_files=[]

    for i in lines:
        line_id = int(i.split('-')[1])
        for k in range(len(f_text_id_low[f_id.index(i[:5].lower())])):
            if f_text_id_low[f_id.index(i[:5].lower())][k]<line_id and f_text_id_high[f_id.index(i[:5].lower())][k]>line_id:
                for j in range(len(f_text[f_id.index(i[:5].lower())][k])):
                                if i in f_text[f_id.index(i[:5].lower())][k][j]:
                                    p=j-1
                                    temp=[]
                                    while '</DOC>' not in f_text[f_id.index(i[:5].lower())][k][p]:
                                        temp.append(f_text[f_id.index(i[:5].lower())][k][p])
                                        p+=1
                                    temp.append('</DOC>')
                                    doc.append(temp)
                                    break
                break

    return doc   

            
def extract_fr(lines):
    doc = []

    f_text = []
    f_id = []

    for i in os.listdir('fr94'):
        for j in os.listdir('fr94'+'/'+i):
            f = open('fr94/'+i+'/'+j)
            f_text.append(f.read().splitlines())
            f_id.append(j)


    for i in lines:
        for j in range(len(f_text[f_id.index(i.split('-')[0].lower())])):

            if i in f_text[f_id.index(i.split('-')[0].lower())][j]:
                p=j-1
                temp = []
                while '</DOC>' not in f_text[f_id.index(i.split('-')[0].lower())][p]:
                    temp.append(f_text[f_id.index(i.split('-')[0].lower())][p])
                    p+=1
                temp.append('</DOC>')
                doc.append(temp)
                break



    return doc

def extract_fb(lines):
    doc = []

    text_3 = []
    text_4 = []
    fid_3 = []
    fid_4 = []

    for i in os.listdir('fbis'):
        f = open('fbis/'+i)
        if i[2]=='3':
            temp = f.read().splitlines()
            text_3.append(temp)
            p=0
            while '<DOCNO>' not in temp[p]:
                p+=1
            fid_3.append(int(temp[p].split(' ')[1].split('-')[1]))
        else:
            temp = f.read().splitlines()
            text_4.append(temp)
            p=0
            while '<DOCNO>' not in temp[p]:
                p+=1
            fid_4.append(int(temp[p].split(' ')[1].split('-')[1]))

    for i in lines:
        if i[4]=='3':
            pid=0
            do=False
            while True:
                if len(fid_3)==pid:
                    do=True
                    break
                if int(i.split('-')[1])<fid_3[pid]:
                    pid = pid-1
                    break
                pid+=1
            if not do:
                for j in range(len(text_3[pid])):
                    if i in text_3[pid][j]:
                        p=j-1
                        temp=[]
                        while '</DOC>' not in text_3[pid][p]:
                            temp.append(text_3[pid][p])
                            p+=1
                        temp.append('</DOC>')
                        doc.append(temp)
                        break
            else:
                doc.append([''])
        else:
            pid=0
            while True:
                if int(i.split('-')[1])<fid_4[pid]:
                    pid = pid-1
                    break
                pid+=1
            for j in range(len(text_4[pid])):
                if i in text_4[pid][j]:
                    p=j-1
                    temp = []
                    while '</DOC>' not in text_4[pid][p]:
                        temp.append(text_4[pid][p])
                        p+=1
                    temp.append('</DOC>')
                    doc.append(temp)
                    break

    return doc

#filenames = os.listdir('Evaluations/')

#for i in filenames:
#    if 'results.trec' in i:
#        results.append(i)

f = open(results, "r")
r_text=f.read().splitlines()
    
top_15 = []
    
for k in r_text:
    cline=k.split()
    top_15.append(cline[0]+' '+cline[2])
        
os.system('rm -r Texts')
os.system('mkdir Texts')

with open('Texts/top_15.titles-only.txt', 'w') as f:
    for item in top_15:
        f.write("%s\n" % item)

filenames = os.listdir('Texts/')
top = []

#for i in filenames:
#    if 'top_15' in i:
#        top.append(i)
        
top = ['top_15.titles-only.txt']

a=0
print('Exporting texts...')
for i in top:
    f = open('Texts/'+i, "r")
    fr = []
    ft = []
    fb = []
    la = []
    fr_ids = []
    ft_ids = []
    fb_ids = []
    la_ids = []
    rlines = f.read().splitlines()
    final = []

    lines = []
    lineID = []
    for j in rlines:
        cline=j.split()
        lines.append(cline[-1])
        lineID.append(int(cline[0]))

    for j in range(len(lines)):
        if 'FR' in lines[j]:
            fr.append(lines[j])
            fr_ids.append(lineID[j])
        if 'FT' in lines[j]:
            ft.append(lines[j])
            ft_ids.append(lineID[j])
        if 'FBIS' in lines[j]:
            fb.append(lines[j])
            fb_ids.append(lineID[j])
        if 'LA' in lines[j]:
            la.append(lines[j])
            la_ids.append(lineID[j])
        a+=1
    print('Exporting fr...')
    fr = extract_fr(fr)
    print('Exporting ft...')
    ft = extract_ft(ft)
    print('Exporting fbis...')
    fb = extract_fb(fb)
    print('Exporting latimes...')
    la = extract_la(la)

    fr_id = 0
    ft_id = 0
    fb_id = 0
    la_id = 0
    queries = []
    for j in range(301,451):
        current = []

        if fr_id != len(fr_ids):
            while fr_ids[fr_id]==j:
                current = current + fr[fr_id]
                fr_id+=1
                if fr_id == len(fr_ids):
                    break
        if ft_id != len(ft):
            while ft_ids[ft_id]==j:
                current = current + ft[ft_id]
                ft_id+=1
                if ft_id == len(ft):
                    break
        if fb_id != len(fb):                
            while fb_ids[fb_id]==j:
                current = current + fb[fb_id]
                fb_id+=1
                if fb_id == len(fb_ids):
                    break
        if la_id != len(la_ids):               
            while la_ids[la_id]==j:
                current = current + la[la_id]
                la_id+=1
                if la_id == len(la_ids):
                    break

        queries.append(current)

all_words=[]
for k in range(len(queries)):
    c_text = ''
    for i in queries[k]:
        c_text = c_text + i
    c_text = Counter(c_text.strip().split())
    all_words.append(c_text.most_common())

stopwords = set(nltk.corpus.stopwords.words('english'))

c_stopwords = list(stopwords)[:]

for i in range(len(c_stopwords)):
    c_stopwords[i] = c_stopwords[i][0].upper()+c_stopwords[i][1:]

c_stopwords = set(c_stopwords)

eng_words = words.words()

final_words = []
final_syn = []
final_words_enriched = []

for query in range(len(all_words)):
    temp = []
    for i in all_words[query]:
        word = i[0]
        for k in ['<','>','/','.',',','"',"'",':',')','(',' ']:
            word = word.replace(k,'')
        if not use_stopwords and word not in stopwords and word not in c_stopwords and len(word)>2 and word in eng_words:
            temp.append(word)
        else:
            if word in eng_words:
                temp.append(word)
        if len(temp)==20:
            break

    f = []
    for i in range(len(temp)):
        synonyms = []
        for syn in nltk.corpus.wordnet.synsets(temp[i]):
            for l in syn.lemmas():
                synonyms.append(l.name())
        synonyms.append(temp[i])
        synonyms = list(set(synonyms))
        f = f + synonyms

    t = list(set(f))
    f = ''
    for i in t:
        f = f + ' ' + i
    final_words_enriched.append(f)

    f = ''
    for i in temp:
        f = f+ ' '+i
    final_words.append(f)

    f = []
    for i in range(len(temp)):
        synonyms = []
        for syn in nltk.corpus.wordnet.synsets(temp[i]):
            for l in syn.lemmas():
                synonyms.append(l.name())
        synonyms = list(set(synonyms))
        f = f + synonyms
        
    t = list(set(f))
    f = ''
    for i in t:
        f = f + ' ' + i
    final_syn.append(f)

f = open(query_file_name, "r")
query_file=f.read().splitlines()

import random
for i in range(len(final_syn)):
    final_syn[i] = ' '.join(random.sample(final_syn[i].split(),int(len(final_syn[i].split())/2)))

ftemp = []
for i in query_file:
    ftemp.append(i)
    if '<rule>' in i:
        ftemp.append('<retModel>indri</retModel> <fbMu>0.0</fbMu> <fbOrigWeight>'+str(fbOrigWeight)+'</fbOrigWeight>')
query_file = ftemp[:]
query_file_syns_only = ftemp[:]
query_file_syns = ftemp[:]

query_num = 0
for i in range(len(query_file)):
    if '<query>' in query_file[i]:
        query_file[i] = query_file[i][:query_file[i].index('<text>')+6]+query_file[i][query_file[i].index('<text>')+6:query_file[i].index('</text>')] + final_words[query_num] +  query_file[i][query_file[i].index('</text>'):]
        query_num+=1
        
query_num = 0
for i in range(len(query_file_syns)):
    if '<query>' in query_file_syns[i]:
        query_file_syns[i] = query_file_syns[i][:query_file_syns[i].index('<text>')+6]+query_file_syns[i][query_file_syns[i].index('<text>')+6:query_file_syns[i].index('</text>')] + final_words_enriched[query_num] +  query_file_syns[i][query_file_syns[i].index('</text>'):]
        query_num+=1
        
query_num = 0
for i in range(len(query_file_syns_only)):
    if '<query>' in query_file_syns_only[i]:
        query_file_syns_only[i] = query_file_syns_only[i][:query_file_syns_only[i].index('<text>')+6]+query_file_syns_only[i][query_file_syns_only[i].index('<text>')+6:query_file_syns_only[i].index('</text>')] + final_syn[query_num] +  query_file_syns_only[i][query_file_syns_only[i].index('</text>'):]
        query_num+=1        

with open(query_file_name.split('/')[-1].replace('.ERGASIA','-RF.ERGASIA').replace('.EXAMPLE','-RF.EXAMPLE'), 'w') as f:
    for item in query_file:
        f.write("%s\n" % item)

with open(query_file_name.split('/')[-1].replace('.ERGASIA','-RF-SYN.ERGASIA').replace('.EXAMPLE','RF-SYN.EXAMPLE'), 'w') as f:
    for item in query_file_syns:
        f.write("%s\n" % item)
        
with open(query_file_name.split('/')[-1].replace('.ERGASIA','-ONLY-SYN.ERGASIA').replace('.EXAMPLE','-ONLY-SYN.EXAMPLE'), 'w') as f:
    for item in query_file_syns_only:
        f.write("%s\n" % item)