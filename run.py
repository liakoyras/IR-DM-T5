import os
import time
from collections import Counter
import nltk
nltk.download('stopwords')
nltk.download('wordnet')

def output_folder():
    cd = os.listdir('.')

    if 'OUTPUT' in cd:
        os.system('rm -r OUTPUT')
    if 'Texts' in cd:
	os.system('rm -r Texts')

    os.system('mkdir OUTPUT')

    
def ask_Y_N(question):
    answer = ' '
    answers = ['Y', 'y', 'N', 'n']
    while answer not in answers:
        answer = raw_input(question +' (y/n): ')
    return answer


def create_index(cd,file):
    d = raw_input('Enter folder name for storing indexes: ')
    
    print('Building Indexes')
    os.system('IndriBuildIndex ' + file)
    
    print('Dumping Indexes')
    os.system('dumpindex '+ cd + '/' + d +' v')
    
    return cd + '/' + d


def get_index():
    return raw_input('Enter folder name with stored indexes: ')


def create_final_adhoc():
    lines = []
    full_adhoc = 'OUTPUT/final.trec.adhoc'
    
    for i in os.listdir('.'):
        if 'adhoc' in i:
            f = open(i, "r")
            lines=lines+f.read().splitlines()

    with open(full_adhoc, 'w') as f:
        for item in lines:
            f.write("%s\n" % item)
    return full_adhoc


def create_queries(index_dir):
    lines=[]

    for i in os.listdir('.'):
        if 'topics' in i:
            f = open(i, "r")
            lines = lines + f.read().splitlines()

    titles = []
    desc = []
    nar = []

    i=0
    while i < len(lines):
        if '<title>' in lines[i]:
            titles.append(lines[i][7:])
        if '<desc>' in lines[i]:
            i=i+1
            temp = ''
            while '<narr>' not in lines[i]:
                temp = temp + ' ' +lines[i]
                i=i+1
            desc.append(temp)
        if '<narr>' in lines[i]:
            i=i+1
            temp = ''
            while '</top>' not in lines[i]:
                temp = temp + lines[i]
                i=i+1
            nar.append(temp)
        i+=1

    for i in range(0,len(titles)):
        titles[i]=titles[i][1:-1]
        desc[i]=desc[i][1:-1]
    for i in range(0,len(titles)):
        for j in ['.'  ,',' , '!', '?', '-', '(', ')', "'", '"', '/', '[' , ']', '{', '}' , '+', '%', '#', '@','$','^','&','*','_','|',';',':','  ']:
            titles[i]=titles[i].replace(j,' ')
            desc[i]=desc[i].replace(j,' ')
            nar[i]=nar[i].replace(j,' ')

    size = raw_input('Enter number of returned texts (example 15): ')
     
    for i in os.listdir('.'):
        if ('IndriRunQuery' in i) and ('EXAMPLE' in i):
            f = open(i, "r")
            prmv = f.read().splitlines()
	    for n in range(len(prmv)):
                if '<count>' in prmv[n]:
                    prmv[n] = prmv[n].replace('1000',size)
		    break
		
	    with open('OUTPUT/'+i, 'w') as f:
                for item in prmv:
                    f.write("%s\n" % item) 
    
    final = ['<parameters>','<index>'+index_dir+'</index>','<rule>method:dirichlet,mu:1000</rule>','<count>'+size+'</count>','<trecFormat>true</trecFormat>']
    num = 301
    for i in range(0,len(titles)):
        final = final + ['<query> <type>indri</type> <number>'+str(num)+'</number> <text>'+titles[i]+' '+desc[i]+'</text> </query>']
        num+=1
    final = final + ['</parameters>']
    
    sname = 'OUTPUT/IndriRunQuery.queries.file.301-450-titles-descs.ERGASIA'

    with open(sname, 'w') as f:
        for item in final:
            f.write("%s\n" % item)
    
    final = ['<parameters>','<index>'+index_dir+'</index>','<rule>method:dirichlet,mu:1000</rule>','<count>'+size+'</count>','<trecFormat>true</trecFormat>']
    num = 301
    for i in range(0,len(titles)):
        final = final + ['<query> <type>indri</type> <number>'+str(num)+'</number> <text>'+titles[i]+' '+desc[i]+' '+nar[i]+'</text> </query>']
        num+=1
    final = final + ['</parameters>']
    
    sname = 'OUTPUT/IndriRunQuery.querries.file.301-450-titles-descs-nars.ERGASIA'

    with open(sname, 'w') as f:
        for item in final:
            f.write("%s\n" % item)

            
def run_queries(current_dir,full_adhoc):
    filenames=[]

    if ask_Y_N('Do you want to create RF model from old result file?') in ['Y','y']:
        build_RF()

    for i in os.listdir('.'):
        if ('IndriRunQuery' in i) and ('RF' in i):
            f = open(i, "r")
            prmv = f.read().splitlines()
	    for n in range(len(prmv)):
                if '<count>' in prmv[n]:
                    prmv[n] = prmv[n].replace('15','1000')
		    break
		
	    with open('OUTPUT/'+i, 'w') as f:
                for item in prmv:
                    f.write("%s\n" % item) 
            
    for i in os.listdir('OUTPUT'):
        if 'IndriRunQuery' in i:
            filenames.append('OUTPUT/'+i)

    os.system('mkdir Evaluations') 

    print('Found '+str(len(filenames))+' query files!')       
            
    for i in filenames:
        if ask_Y_N('Do you want to run the query file "'+i+'"?') in ['Y','y']:
            print('Searching with and evaluating: '+i.split('.')[-2])
            fname = i.split('.')[-2]+'-results.trec'
            os.system('IndriRunQuery '+i+' > Evaluations/'+ fname)
        else:
            print('Skipping query file: '+i.split('.')[-2])

    filenames = []

    for i in os.listdir('Evaluations'):
        if 'results.trec' in i:
            filenames.append('Evaluations/'+i)

    print('Found '+str(len(filenames))+' query results!')

    for i in filenames:
        if ask_Y_N('Do you want to evaluate the results file "'+i.split('/')[-1]+'"?') in ['Y','y']:
            print('Evaluating: '+i.split('/')[-1])
            os.system('trec_eval ' + current_dir + '/' + full_adhoc + ' ' + current_dir + '/'+ i + ' > ' + i[:-4] + 'eval')
        else:
            print('Skipping results file: '+i.split('/')[-1])
            
            
def time_extraction(fun,args):
    start = time.time()
    fun(args)
    return time.time()-start


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
            while True:
                if int(i.split('-')[1])<fid_3[pid]:
                    pid = pid-1
                    break
                pid+=1
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

def build_RF():
    filenames = os.listdir('Evaluations/')
    results = []
    
    for i in filenames:
        if 'results.trec' in i:
            results.append(i)
    
    done=False
    while not done:
        for i in results:
            if ask_Y_N('Build RF for result file: '+i+' ?') in ['Y','y']:
                results = [i]
                done = True
                break
                
    qfilenames = os.listdir('OUTPUT/')
    
    qresults=[]
    for i in qfilenames:
        if 'IndriRunQuery' in i:
            qresults.append(i)

    done=False
    while not done:
        for i in qresults:
            if ask_Y_N('Is : '+i+' the correct query file to append?') in ['Y','y']:
                query_file_name = 'OUTPUT/'+i
                done = True
                break

    r_text = []

    for i in results:
        f = open('Evaluations/'+i, "r")
        r_text.append(f.read().splitlines())


    pt = 301
    for k in range(len(r_text)):
        i = 0
        split = []
        lines = r_text[k]
        for i in range(0, len(lines)):
            split = split + lines[i].split()

        j = 0
        i = 0
        top_15 = []
        for i in range(2,len(split),6):
            top_15.append(split[2 + j])
            j = j + 6

        os.system('rm -r Texts')
        os.system('mkdir Texts')

        with open('Texts/top_15.'+results[k].split('.')[0]+'.txt', 'w') as f:
            for item in top_15:
                f.write("%s\n" % item)
                
    filenames = os.listdir('Texts/')
    top = []

    for i in filenames:
        if 'top_15' in i:
            top.append(i)
    os.system('rm -r /Texts/sorted')

    a=0
    q=301
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
        lines = f.read().splitlines()
        final = []
        for j in range(len(lines)):
            if 'FR' in lines[j]:
                fr.append(lines[j])
                fr_ids.append(q-301)
            if 'FT' in lines[j]:
                ft.append(lines[j])
                ft_ids.append(q-301)
            if 'FBIS' in lines[j]:
                fb.append(lines[j])
                fb_ids.append(q-301)
            if 'LA' in lines[j]:
                la.append(lines[j])
                la_ids.append(q-301)
            a+=1
            if a==15:
                a=0
                q+=1
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
        for j in range(150):
            current = []

            if fr_id != len(fr):
                while fr_ids[fr_id]==j:
                    current = current + fr[fr_id]
                    fr_id+=1
                    if fr_id == len(fr):
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
                    if fb_id == len(fb):
                        break
            if la_id != len(la):               
                while la_ids[la_id]==j:
                    current = current + la[la_id]
                    la_id+=1
                    if la_id == len(la):
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

    final_words = []
    final_words_enriched = []

    for query in range(len(all_words)):
        temp = []
        for i in all_words[query]:
            word = i[0].lower()
            for k in ['<','>','/','.',',','"',"'",'-','_']:
                word = word.replace(k,'')
            if word not in stopwords and len(word)>2:
                temp.append(word)
            if len(temp)==15:
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
        
    f = open(query_file_name, "r")
    query_file=f.read().splitlines()
    weight = raw_input('Enter the weight (decimal - example: 0.5) for "fbOrigWeight": ')
    ftemp = []
    for i in query_file:
        ftemp.append(i)
        if '<rule>' in i:
            ftemp.append('<retModel>Indri</retModel> <fbMu>0.0</fbMu> <fbOrigWeight>'+weight+'</fbOrigWeight>')
    query_file = ftemp[:]
    query_file_syns = ftemp[:]

    query_num = 0
    for i in range(len(query_file)):
        if '<query>' in query_file[i]:
            query_file[i] = query_file[i][:query_file[i].index('<text>')+6]+' '.join(list(set(((query_file[i][query_file[i].index('<text>')+6:query_file[i].index('</text>')].lower() + final_words[query_num]).split())))) +  query_file[i][query_file[i].index('</text>'):]

    query_num = 0
    for i in range(len(query_file_syns)):
        if '<query>' in query_file_syns[i]:
            query_file_syns[i] = query_file_syns[i][:query_file_syns[i].index('<text>')+6]+' '.join(list(set(((query_file_syns[i][query_file_syns[i].index('<text>')+6:query_file_syns[i].index('</text>')] + final_words_enriched[query_num]).split())))) +  query_file_syns[i][query_file_syns[i].index('</text>'):]

    with open(query_file_name.split('/')[-1].replace('.ERGASIA','-RF.ERGASIA').replace('.EXAMPLE','-RF.EXAMPLE'), 'w') as f:
        for item in query_file:
            f.write("%s\n" % item)

    with open(query_file_name.split('/')[-1].replace('.ERGASIA','-RF-SYN.ERGASIA').replace('.EXAMPLE','RF-SYN.EXAMPLE'), 'w') as f:
        for item in query_file_syns:
            f.write("%s\n" % item)

output_folder()
current_dir = os.path.abspath(os.getcwd())

if ask_Y_N('Do you want to create the Indexes?') in ['Y','y']:
    BIF = []
    for i in os.listdir('.'):
        if 'IndriBuildIndex' in i:
            BIF.append(i)
    
    done=False
    while not done:
        for i in BIF:
            if ask_Y_N('Build with file: '+i+' ?') in ['Y','y']:
                index_dir = create_index(current_dir,i)
                done = True
                break
else:
    index_dir = current_dir + '/' + get_index()
    
full_adhoc = create_final_adhoc()
create_queries(index_dir=index_dir)
run_queries(current_dir=current_dir,full_adhoc=full_adhoc)
