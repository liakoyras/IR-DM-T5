import os
import time

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

filenames = os.listdir('Evaluations/')
results = []

for i in filenames:
    if 'results.trec' in i:
        results.append(i)
        
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
filenum = 0
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
    fr = extract_fr(fr)
    ft = extract_ft(ft)
    fb = extract_fb(fb)
    la = extract_la(la)
    
    fr_id = 0
    ft_id = 0
    fb_id = 0
    la_id = 0
    for j in range(150):
        current = []
        print(j)
        
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
        if fb_id != len(fb_ids):                
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
            
        os.system('mkdir Texts/'+str(filenames[filenum])[:-4].replace('.','_'))
        with open('Texts/'+str(filenames[filenum])[:-4].replace('.','_')+'/'+str(j)+'.txt', 'w') as f:
            for item in current:
                f.write("%s\n" % item)    
    
    filenum+=1