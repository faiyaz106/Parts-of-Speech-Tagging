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

single_word_list=[]   # To store the single occurence word

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

s_w_t_p=[]     # contains the list of tag which occured in single occurence word
for i in single_word_list:
    for j in single_tag.keys():
        s_w_t=i+' '+j
        if s_w_t in word_tag.keys():
            s_w_t_p.append(j)
        else:
            continue


s_w_p_d={}  # To store the tag along with the count for the single occurence word
for i in s_w_t_p:
    if i not in s_w_p_d.keys():
        s_w_p_d[i]=1
    else:
        s_w_p_d[i]=s_w_p_d[i]+1

count_list=[]
for i in s_w_p_d.keys():
    count_list.append(s_w_p_d[i])

for i in range(0,len(count_list)-1):
    idx=i
    for j in range(i+1,len(count_list)):
        if count_list[j]>count_list[idx]:
            idx=j
        else:
            continue
    temp=count_list[i]
    count_list[i]=count_list[idx]
    count_list[idx]=temp

top_5_tag=[]  # Store the top 5 tag which occured in single occurence word


for i in range(0,5):
    for j in s_w_p_d.keys():
        if s_w_p_d[j]==count_list[i]:
            top_5_tag.append(j)
        else:
            continue


def check_zero_prob(arr):
    n=len(arr)
    output=True
    for i in range(0,n):
        if arr[i][-1]>0:
            output=False
            break
        else:
            continue
    return output


def initialization(first_word,single_tag,bigram_tag,word_tag,s_w_p_d,top_5_tag):
    first_list=[]
    v=len(single_tag)
    for j in single_tag.keys():
        l=[]
        if j!= '<s>':
            w_t=str(first_word)+' '+str(j)
            if w_t in word_tag.keys():
                p_w_t=word_tag[w_t][1]
            else:
                p_w_t=0
            t_t='<s>'+' '+str(j)
            if t_t in bigram_tag.keys():
                p_t_t=bigram_tag[t_t][1]
            else:
                p_t_t=0
        else:
             continue
        score=p_w_t*p_t_t
        l.append((first_word,j))
        l.append(score)
        first_list.append(l)
    if check_zero_prob(first_list):
        new_list=[]
        v=len(single_tag)
        t=top_5_tag
        for i in t:
            temp=[]
            tag=i
            p_w_t=s_w_p_d[i]/single_tag[i]
            t_t='<s>'+' '+str(tag)
            if t_t in bigram_tag.keys():
                p_t_t=bigram_tag[t_t][1]/single_tag[tag]
            else:
                p_t_t=0
            score=p_w_t*p_t_t
            temp.append((first_word,tag))
            temp.append(score)
            new_list.append(temp)
        return new_list

    else:
        return first_list


def back_ptr(tag,prev_tag,bigram_tag):
    n=len(prev_tag[0])
    list=[]
    for i in range(0,len(prev_tag)):
        l=[]
        pt_ct=str(prev_tag[i][n-2][1])+' '+str(tag)
        if pt_ct in bigram_tag:
            p_pt_ct=bigram_tag[pt_ct][1]
        else:
            p_pt_ct=0
        score=prev_tag[i][n-1]*p_pt_ct
        list.append(score)
    max_=max(list)
    index=list.index(max_)
    return max_,index

def zero_prob_h(tag,prev_tag,bigram_tag,single_tag):
    n=len(prev_tag[0])
    v=len(single_tag)
    list=[]
    for i in range(0,len(prev_tag)):
        l=[]
        pt_ct=str(prev_tag[i][n-2][1])+' '+str(tag)
        if pt_ct in bigram_tag:
            p_pt_ct=bigram_tag[pt_ct][1]
        else:
            p_pt_ct=0
        score=prev_tag[i][n-1]*p_pt_ct
        list.append(score)
    max_=max(list)
    index=list.index(max_)
    return max_,index


def viterbi_score(word,single_tag,word_tag,bigram_tag,prev_list,s_w_p_d,top_5_tag):
    c_list=[]
    for j in single_tag.keys():
        temp=[]
        if j!= '<s>':
            w_t=str(word)+' '+str(j)
            if w_t in word_tag.keys():
                p_w_t=word_tag[w_t][1]
            else:
                p_w_t=0
        else:
            continue
        tag=j
        max_score,idx=back_ptr(tag,prev_list,bigram_tag)
        p=p_w_t*max_score
        for m in range(0,len(prev_list[idx])-1):
            temp.append(prev_list[idx][m])
        temp.append((word,j))
        temp.append(p)
        c_list.append(temp)
    if check_zero_prob(c_list):
        new_list=[]
        t=top_5_tag
        for i in t:
            temp=[]
            tag=i
            p_w_t=s_w_p_d[i]/single_tag[i]
            max_score,idx=zero_prob_h(tag,prev_list,bigram_tag,single_tag)
            p=p_w_t*max_score
            for m in range(0,len(prev_list[idx])-1):
                temp.append(prev_list[idx][m])
            temp.append((word,tag))
            temp.append(p)
            new_list.append(temp)

        return new_list
    else:
        return c_list

def max_score_seq(final_list):
    a=final_list
    max_row=0
    n=len(final_list[0])
    for j in range(0,len(final_list)):
        if a[j][n-1]>a[max_row][n-1]:
            max_row=j
        else:
            continue
    return max_row

def viterbi_algo(sentence,single_tag,bigram_tag,word_tag,s_w_p_d,top_5_tag):
    word_token=sentence.split()
    n=len(word_token)
    prev_list=initialization(word_token[0].lower(),single_tag,bigram_tag,word_tag,s_w_p_d,top_5_tag)
    for i in range(1,n):
        word=word_token[i].lower()
        prev_list=viterbi_score(word,single_tag,word_tag,bigram_tag,prev_list,s_w_p_d,top_5_tag)
    final_list=prev_list
    max_row=max_score_seq(final_list)
    final_tagged_seq=final_list[max_row]
    return final_tagged_seq


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
        seq=viterbi_algo(sentence,single_tag,bigram_tag,word_tag,s_w_p_d,top_5_tag)
        for i in range(0,len(seq)-1):
            string=str(seq[i][0])+'/'+str(seq[i][1])
            predicted_data.append(seq[i])


correct_count=0  # To count the correct number of tag
error_data=[]   # Storing the error tagged data
for i in range(0,len(test_data)):
    if test_data[i][1]==predicted_data[i][1]:
        correct_count=correct_count+1

    else:
        error_data.append((test_data[i][0],test_data[i][1],predicted_data[i][1]))


accuracy=correct_count*100/len(test_data)
print('Accuracy:{}%'.format(accuracy))

f=open('POS.test.out','x')
#For writing text file on the created text file
n=len(test_data)
for i in range(0,n):
    text=''
    text=str(test_data[i][0])+' '+str(predicted_data[i][1])+'\n'
    f.write(text)
