import os


def output_folder():
    cd = os.listdir('.')

    if 'OUTPUT' in cd:
        os.system('rm -r OUTPUT')

    os.system('mkdir OUTPUT')

    
def ask_Y_N(question):
    answer = ' '
    answers = ['Y', 'y', 'N', 'n']
    while answer not in answers:
        answer = raw_input(question +' (y/n): ')
    return answer


def create_index(cd):
    d = raw_input('Enter folder name for storing indexes: ')
    
    print('Building Indexes')
    os.system('IndriBuildIndex IndriBuildIndex.parameter.file.EXAMPLE')
    
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

    critical_answer = ask_Y_N('Run with RF model?')
	
    if critical_answer in ['Y','y']:
	needed = '<retModel>indri</retModel> <fbDocs>15</fbDocs> <fbTerms>20</fbTerms> <fbMu>0.5</fbMu> <fbOrigWeight>0.5</fbOrigWeight>'
        for i in os.listdir('.'):
            if 'IndriRunQuery' in i:	
                f = open(i, "r")
                example=f.read().splitlines()
                for lnum in range(len(example)):
                    if '<rule>' in example[lnum]:
                        final = example[:lnum+1]
                        final = final + [needed]
                        final = final + example[lnum+2:]
                        break
                with open('OUTPUT/'+i, 'w') as f:
                    for item in final:
                        f.write("%s\n" % item)
    else:
        for i in os.listdir('.'):
            if 'IndriRunQuery' in i:
                os.system('cp '+i+' OUTPUT/'+i)
		
    if critical_answer in ['Y','y']:
        final = ['<parameters>','<index>'+index_dir+'</index>','<retModel>indri</retModel>','<fbDocs>15</fbDocs> <fbTerms>20</fbTerms> <fbMu>0.5</fbMu> <fbOrigWeight>0.5</fbOrigWeight>','<rule>method:dirichlet,mu:1000</rule>','<count>1000</count>','<trecFormat>true</trecFormat>']        
    else:
        final = ['<parameters>','<index>'+index_dir+'</index>','<rule>method:dirichlet,mu:1000</rule>','<count>1000</count>','<trecFormat>true</trecFormat>']
    num = 301
    for i in range(0,len(titles)):
        final = final + ['<query> <type>indri</type> <number>'+str(num)+'</number> <text>'+titles[i]+' '+desc[i]+'</text> </query>']
        num+=1
    final = final + ['</parameters>']

    with open('OUTPUT/IndriRunQuery.queries.file.301-450-titles-descs.ERGASIA', 'w') as f:
        for item in final:
            f.write("%s\n" % item)
    
    if critical_answer in ['Y','y']:
        final = ['<parameters>','<index>'+index_dir+'</index>','<retModel>indri</retModel>','<fbDocs>15</fbDocs> <fbTerms>20</fbTerms> <fbMu>0.5</fbMu> <fbOrigWeight>0.5</fbOrigWeight>','<rule>method:dirichlet,mu:1000</rule>','<count>1000</count>','<trecFormat>true</trecFormat>']        
    else:
        final = ['<parameters>','<index>'+index_dir+'</index>','<rule>method:dirichlet,mu:1000</rule>','<count>1000</count>','<trecFormat>true</trecFormat>']
    num = 301
    for i in range(0,len(titles)):
        final = final + ['<query> <type>indri</type> <number>'+str(num)+'</number> <text>'+titles[i]+' '+desc[i]+' '+nar[i]+'</text> </query>']
        num+=1
    final = final + ['</parameters>']

    with open('OUTPUT/IndriRunQuery.queries.file.301-450-titles-descs-nars.ERGASIA', 'w') as f:
        for item in final:
            f.write("%s\n" % item)

            
def run_queries(current_dir,full_adhoc):
    filenames=[]

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
#====#

output_folder()
current_dir = os.path.abspath(os.getcwd())

if ask_Y_N('Do you want to create the Indexes?') in ['Y','y']:
    index_dir = create_index(current_dir)
else:
    index_dir = current_dir + '/' + get_index()
    
full_adhoc = create_final_adhoc()
create_queries(index_dir=index_dir)
run_queries(current_dir=current_dir,full_adhoc=full_adhoc)
