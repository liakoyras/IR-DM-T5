import os

current_dir = os.path.abspath(os.getcwd())
index_dir = current_dir + '/indices'

cd = os.listdir('.')

if 'OUTPUT' in cd:
  os.system('rm -r OUTPUT')
  
os.system('mkdir OUTPUT')

print('Building Indexes')
os.system('IndriBuildIndex IndriBuildIndex.parameter.file.EXAMPLE')
print('Dumping Indexes')
os.system('dumpindex '+ index_dir +' v')

lines = []
full_adhoc = 'OUTPUT/final.trec.adhoc'

for i in os.listdir('.'):
    if 'adhoc' in i:
        f = open(i, "r")
        lines=lines+f.read().splitlines()
        
with open(full_adhoc, 'w') as f:
    for item in lines:
        f.write("%s\n" % item)

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

final = ['<parameters>','<index>'+index_dir+'</index>','<rule>method:dirichlet,mu:1000</rule>','<count>1000</count>','<trecFormat>true</trecFormat>']
num = 301
for i in range(0,len(titles)):
    final = final + ['<query> <type>indri</type> <number>'+str(num)+'</number> <text>'+titles[i]+' '+desc[i]+'</text> </query>']
    num+=1
final = final + ['</parameters>']

with open('OUTPUT/IndriRunQuery.queries.file.301-450-titles-descs.ERGASIA', 'w') as f:
    for item in final:
        f.write("%s\n" % item)

final = ['<parameters>','<index>'+index_dir+'</index>','<rule>method:dirichlet,mu:1000</rule>','<count>1000</count>','<trecFormat>true</trecFormat>']
num = 301
for i in range(0,len(titles)):
    final = final + ['<query> <type>indri</type> <number>'+str(num)+'</number> <text>'+titles[i]+' '+desc[i]+' '+nar[i]+'</text> </query>']
    num+=1
final = final + ['</parameters>']

with open('OUTPUT/IndriRunQuery.querries.file.301-450-titles-descs-nars.ERGASIA', 'w') as f:
    for item in final:
        f.write("%s\n" % item)

filenames=[]

for i in os.listdir('.'):
  if 'IndriRunQuery' in i:
    os.system('cp '+i+' OUTPUT/'+i)

for i in os.listdir('OUTPUT'):
  if 'IndriRunQuery' in i:
    filenames.append('OUTPUT/'+i)

for i in filenames:
  print('Searching with and evaluating: '+i.split('.')[-2])
  fname = i.split('.')[-2]+'-results.trec'
  os.system('IndriRunQuery '+i+' > OUTPUT/'+ fname)
  os.system('trec_eval ' + current_dir + '/' + full_adhoc + ' ' + current_dir + '/OUTPUT/' + fname + ' > OUTPUT/' + fname[:-4] + 'eval')


