import sys
f=open(sys.argv[1],'r')

single_tag={}   # For storing single tag including '<s>' as start of sentence
word_tag={}     # Storing the 'Word Tag' sequence along with count and probability
tag_list=[]     # To store the list of tag sentence wise.
bigram_tag={}   # To store the 'Previous_Tag  Current_Tag' along with the count and probability
unique_word={}  # Storing all the unique word with count

for i in f:
    tag_list.append('<s>')
    if '<s>' not in single_tag.keys():
        single_tag['<s>']=1
    else:
        single_tag['<s>']=single_tag['<s>']+1
    for j in i.split():
        k=j.split('/')
        n=len(k)
        if (n>1) and (k[n-1].isalpha()) and (k[n-2] is not ' '):
            w_t_pair=k[n-2].lower()+' '+k[n-1]
            if k[n-1].isupper():
                if k[n-2].lower() not in unique_word:
                    unique_word[k[n-2].lower()]=1
                else:
                    unique_word[k[n-2].lower()]=unique_word[k[n-2].lower()]+1
                tag_list.append(k[n-1])
                if k[n-1] not in single_tag.keys():
                    single_tag[k[n-1]]=1
                else:
                    single_tag[k[n-1]]=single_tag[k[n-1]]+1

                if w_t_pair not in word_tag.keys():
                    word_tag[w_t_pair]=[]
                    word_tag[w_t_pair].append(1)
                else:
                    word_tag[w_t_pair][0]=word_tag[w_t_pair][0]+1
        else:
            continue

for i in range(0,len(tag_list)-1):
    if tag_list[i+1] is not '<s>':
        key=str(tag_list[i])+' '+str(tag_list[i+1])
    else:
        continue
    if key not in bigram_tag.keys():
        bigram_tag[key]=[]
        bigram_tag[key].append(1)
    else:
        bigram_tag[key][0]=bigram_tag[key][0]+1

for i in bigram_tag.keys():
    j=i.split()
    prob=bigram_tag[i][0]/single_tag[j[0]]
    bigram_tag[i].append(prob)

single_word_list=[]

for i in word_tag.keys():
    j=i.split()
    n=len(j)
    prob=word_tag[i][0]/single_tag[j[n-1]]
    word_tag[i].append(prob)

for i in unique_word.keys():
    if unique_word[i]==1:
        single_word_list.append(str(i))
    else:
        continue
single_word_tag={}

for i in word_tag.keys():
    if word_tag[i]==1:
        i=i.split()
        if i[1] not in single_word_tag.keys():
            single_word_tag[i[1]]=1
        else:
            single_word_tag[i[1]]=single_word_tag[i[1]]+1
    else:
        continue
s_w_t_p=[]
for i in single_word_list:
    for j in single_tag.keys():
        s_w_t=i+' '+j
        if s_w_t in word_tag.keys():
            s_w_t_p.append(j)
        else:
            continue

s_w_p_d={}
for i in s_w_t_p:
    if i not in s_w_p_d.keys():
        s_w_p_d[i]=1
    else:
        s_w_p_d[i]=s_w_p_d[i]+1

key_list=list(s_w_p_d.keys())
max_key=key_list[0]
for j in s_w_p_d.keys():
    if s_w_p_d[j]>s_w_p_d[max_key]:
        max_key=j
    else:
        continue

def baseline(sentence,bigram_tag,single_tag,word_tag,s_w_p_d,max_key):
    word_token=sentence.split()
    seq=[]
    for i in word_token:
        p_w_t=0
        for j in single_tag.keys():
            w_t=i+' '+j
            if w_t in word_tag.keys():
                if p_w_t<word_tag[w_t][1]:
                    p_w_t=word_tag[w_t][1]
                    tag=j
            else:
                continue
        if p_w_t==0:
            tag=max_key
        seq.append((i,tag))
    return seq


test_data=[]  # To store the word and actual tag of test data
predicted_data=[]  # To store the word and predicted tag on test data

f=open(sys.argv[2],'r')

for i in f:
    sentence=''
    for j in i.split():
        temp=[]
        k=j.split('/')
        n=len(k)
        if (n>1) and (k[n-1].isalpha()) and (k[n-2] is not '' ):
            test_data.append((k[n-2],k[n-1]))
            sentence=sentence+' '+str(k[n-2])
    if sentence is '':
        continue
    else:
        seq=baseline(sentence,bigram_tag,single_tag,word_tag,s_w_p_d,max_key)
        for i in range(0,len(seq)):
            predicted_data.append(seq[i])


correct_count=0  # To store the correctly predicted tag
for i in range(0,len(predicted_data)):
    if test_data[i][1]==predicted_data[i][1]:
        correct_count=correct_count+1
    else:
        continue

accuracy=correct_count*100/len(test_data)
print('Accuracy:',accuracy)
