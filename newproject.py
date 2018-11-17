import json
import nltk
import re
from nltk.corpus import names
from gensim.summarization import bm25
from nltk.corpus import  stopwords
from nltk.chunk import tree2conlltags
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk.tokenize import sent_tokenize
import csv
import spacy
f=open("documents.json")
documentation = json.load(f)
f.close()
f2=open("devel.json")
question=json.load(f2)
f2.close()
f3=open("testing.json")
testing=json.load(f3)
#f3.close()
#f4=open("training.json")
#training=json.load(f4)


question_corpus=["what","What","where","Where","where?","who","Who","who?","whom","Whom","whom?","whose","Whose","whose?","when","When","when?","how","How","how?","which","Which","which?","What's","Does","Do","what?","Why","why","Can","Were","On","In","With","From","Are","Would","Will","Was","Has","Did"]
percentage_question_list=["What percentage","what percentage","How much of","What accounts for","increase","overall incidence","How much inflation","what was the percentage","What percentages","what percentages","How accountable","margin"]
money_question_list=["How much","budget","the amount of the production","income","the value of","average amount","how much","value","salary increase","dollar amount","What was the price"]
data_question_list=["What date","When","what date","which date","what month","How soon"]
year_question_list=["What year","what year","which year","what century","what period"]
person_question_list=["who","Who","who?","whom","Whom","whom?","whose","Whose","whose?"]
Loctaion_question_list=["Where","where","where?","what city","what state","what counrty","what area","what continent","what geographic part","what river","what Province" "what areas" "what street","what neighborhood","what park",
                        "what geographic portion","what district","What location","What country","What state","What county","what geographical location","What region","What area","What areas","What city","What airport","what city","what area","What neighborhood","what country",
                        "what street","what neighborhood","What street","What countries","what country's","What country's","what geographic part","what cities","what Province","what field","which country"]

number_question_list=["How many","how many","How near","How long","How far","How big","How large","How wide","How often","How early","How old","How high","How strong","How recently"]
digital_number=["once","twice","one-","two-","three-","four-","five-","six-","seven-","eight-","nine-","ten-"]



def get_number(aim_sentence):
    aim_words = nltk.word_tokenize(aim_sentence)
    tagged = nltk.pos_tag(aim_words)
    nameEnt = nltk.ne_chunk(tagged, binary=False)
    data_list = []
    for i in nameEnt:
        for k in range(len(i)):
            try:
                if i[k] == "CD":
                    data_list.append(i[k-1])
            except:
                pass
            for digital in digital_number:
                if digital in i[k]:
                    data_list.append(i[k])
            try:
                if re.search("[0-9]+-",i[k]):
                    data_list.append(i[k])
            except:
                pass

    return data_list

def simply(ttk):
    stop_words = set(stopwords.words("english"))
    for word in stopwords.words('english'):
        Uword = word[0].upper() + word[1:]
        stop_words.add(Uword)
    for k in question_corpus:
        stop_words.add(k)
    filtered_doc = list()
    for word_tokens in ttk:
        filtered_sentence = [w for w in word_tokens if not w in stop_words]
        filtered_doc.append(filtered_sentence)
    return filtered_doc
male_name = names.words("male.txt")
female_name = names.words("female.txt")
name = male_name + female_name

def get_date(aim_sentence):
    monthes = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December","january", "february", "march", "april", "may", "june", "july", "august", "september", "october",
               "november", "december"]
    aim_words = nltk.word_tokenize(aim_sentence)
    tagged = nltk.pos_tag(aim_words)
    nameEnt = nltk.ne_chunk(tagged, binary=False)
    data_list = []

    for i in nameEnt:
        for k in range(len(i)):
            try:
                if i[k] == "CD" and int(i[k-1])>0:
                    data_list.append(i[k - 1])
            except:
                pass
            if i[k] in monthes:
                data_list.append(i[k])

    return data_list




def get_year(aim_sentence):
    aim_words = nltk.word_tokenize(aim_sentence)
    tagged = nltk.pos_tag(aim_words)
    nameEnt = nltk.ne_chunk(tagged, binary=False)
    data_list = []
    for i in nameEnt:
        for k in range(len(i)):
            try:
                if i[k] == "CD":
                    data_list.append(i[k-1])
            except:
                pass
    return data_list

def get_percentage(aim_sentence):
    aim_words = nltk.word_tokenize(aim_sentence)
    tagged = nltk.pos_tag(aim_words)
    nameEnt = nltk.ne_chunk(tagged, binary=False)
    data_list = []
    for i in range(len(nameEnt)):
        for k in (nameEnt[i]):
            if k == "%":
                for w in range(len(nameEnt[i-1])):
                    if nameEnt[i-1][w]=="CD":
                        data_list.append(nameEnt[i-1][w-1])
                        data_list.append(k)
    return data_list

def get_money(aim_sentence):
    aim_words = nltk.word_tokenize(aim_sentence)
    tagged = nltk.pos_tag(aim_words)
    nameEnt = nltk.ne_chunk(tagged, binary=False)
    data_list = []
    for i in range(len(nameEnt)):

        for k in (nameEnt[i]):
            if k == "$":
                for w in range(len(nameEnt[i+1])):
                    if i<len(nameEnt)-2:
                        if nameEnt[i+1][w]=="CD" and nameEnt[i+2][w]=="CD":
                            data_list.append(k)
                            data_list.append(nameEnt[i+1][w-1])
                            data_list.append(nameEnt[i+2][w-1])
                            break
                    if i<len(nameEnt)-2:
                        if nameEnt[i+1][w]=="CD" and nameEnt[i+2][w]!="CD":
                            data_list.append(k)
                            data_list.append(nameEnt[i+1][w-1])
                            break
                    if i==len(nameEnt)-2:
                        if nameEnt[i+1][w]=="CD":
                            data_list.append(k)
                            data_list.append(nameEnt[i+1][w-1])
                            break
                break
    return data_list


def get_name(aim_sentence):
    data_list = []
    aim_words = nltk.word_tokenize(aim_sentence)
    tagged = nltk.pos_tag(aim_words)
    nameEnt = nltk.ne_chunk(tagged, binary=False)
    for i in range(len(nameEnt)):
        try:
            if nameEnt[i].label()=="PERSON" and len (nameEnt[i][0])==2 and nameEnt[i+1].label()=="GPE" and len(nameEnt[i+1][0])==2:
                data_list.append(nameEnt[i][0][0])
                data_list.append(nameEnt[i+1][0][0])
        except:
            pass
        try:
            if nameEnt[i].label()=="GPE"and len(nameEnt[i][0])==2 and nameEnt[i+1].label()=="PERSON"and len (nameEnt[i+1][0])==2 :
                data_list.append(nameEnt[i][0][0])
                data_list.append(nameEnt[i+1][0][0])
        except:
            pass
        try:
            if i==len(nameEnt)-1 and nameEnt[i].label()=="PERSON" and len(nameEnt[i][0])==2:
                for k in range(len(nameEnt[i])):
                    data_list.append(nameEnt[i][k][0])
        except:
            pass
        try:
            if i<len(nameEnt)-1 and nameEnt[i].label()=="PERSON" and len(nameEnt[i][0])==2:
                for k in range(len(nameEnt[i])):
                    data_list.append(nameEnt[i][k][0])
        except:
            pass
    if data_list==[]:
        for i in range(len(nameEnt)):
            try:
                if nameEnt[i].label()=="GPE":
                    for k in range(len(nameEnt[i])):
                        data_list.append(nameEnt[i][k][0])
            except:
                pass
            try:
                if nameEnt[i].label()=="ORGANIZATION":
                    for k in range(len(nameEnt[i])):
                        data_list.append(nameEnt[i][k][0])
            except:
                pass
    return list(set(data_list))


#z="In Northeastern France, the area around Calais was historically Dutch-speaking (West Flemish) of which an estimated 20,000 daily speakers"
def get_location(aim_sentence):
    data_list = []
    aim_words = nltk.word_tokenize(aim_sentence)
    tagged = nltk.pos_tag(aim_words)
    nameEnt = nltk.ne_chunk(tagged, binary=False)
    for i in range(len(nameEnt)):
        try:
            if nameEnt[i].label()=="GPE":
                for k in range(len(nameEnt[i])):
                    data_list.append(nameEnt[i][k][0])
        except:
            pass
        try:
            if nameEnt[i].label()=="LOCATION":
                for k in range(len(nameEnt[i])):
                    data_list.append(nameEnt[i][k][0])
        except:
            pass
    return data_list

def whatQuestion(answer,question):
    stop_words = set(stopwords.words("english"))
    for word in stopwords.words('english'):
        Uword = word[0].upper() + word[1:]
        stop_words.add(Uword)
    answer1  = ''
    for word in answer.split():
        if word not in stop_words and word not in question:
            answer1 += word + ' '
#    answer3 = []
#    nlp = spacy.load('en_core_web_sm')
#    doc = nlp(answer1)
#    for chunk in doc.noun_chunks:
#        answer3.append(chunk.text)
    answer2 = tree2conlltags(ne_chunk(pos_tag(word_tokenize(answer1))))
    answer3 = []
    for word in answer2:
        if word[1]=="NN"or word[1] == "NNP":
            answer3.append(word[0])

    return answer3

def find_aim_sentence_time(question_input):
    query_word_list = question_input["question"].split(" ")
    for k in range(len(query_word_list)):
        if (query_word_list[k] == "in" or query_word_list[k] == "In") and re.search("[0-9]{4}", query_word_list[k + 1]):
            year_number = re.findall("[0-9]{4}", query_word_list[k + 1])
            documentation_id = question_input["docid"]
            for word in documentation[documentation_id]["text"]:
                if year_number[0] in word:
                    word_list = word.split(".")
                    for w in word_list:
                        if year_number[0] in w:
                            data_list = w
#                            print("aim_sentence_time",data_list)
                            return data_list
def find_aim_sentence_special(question_input):
    num = []
    name = []
    pos = []
    org = []
    noun = []
    ner_question = tree2conlltags(ne_chunk(pos_tag(word_tokenize(question_input['question']))))
    for word in ner_question:
        if word[1] == 'CD':
            num.append(word[0])
        elif word[2] == 'B-PERSON' or word[2] == 'I-PERSON':
            name.append(word[0])
        elif word[2] == 'B-ORGANIZATION' or word[2] == 'I-ORGANIZATION':
            org.append(word[0])
        elif word[2] == 'B-GPE' or word[2] == 'I-GPE' or word[2] == 'B-LOCATION' or word[2] == 'I-LOCATION':
            pos.append(word[0])
        if word[1] == "NN" or word[1] == "NNP":
            noun.append(word[0])
    ture_sentence =[]
    aim_sentence = BM25_pragrah(question_input)
    all_sent = sent_tokenize(aim_sentence)
    for sent in all_sent:
        flag = set()
        if len(num) > 0:
            for n in num:
                if n in sent:
                    flag.add('Y')
                else:
                    flag.add('N')
        elif len(name) > 0:
            for n in name:
                if n in sent:
                    flag.add('Y')
                else:
                    flag.add('N')
        elif len(org) > 0:
            for o in org:
                if o in sent:
                    flag.add('Y')
                else:
                    flag.add('N')
        elif len(pos) > 0:
            for p in pos:
                if p in sent:
                    flag.add('Y')
                else:
                    flag.add('N')
        i = 0
        for n in noun:
            if n in sent:
                i += 1
        if i > len(noun) * 0.5 and "N" not in flag:
            ture_sentence = sent
#            print("aim",ture_sentence)
    return ture_sentence

def BM25_pragrah(question_input):
    documentation_id=question_input["docid"]
    sentence = []
    corpus = []
    for word in documentation[documentation_id]["text"]:
        sentence.append([word])
    for i in sentence:
        for k in i:
            word_list = k.split(" ")
        corpus.append(word_list)
        word_list = []

    query_str = question_input["question"]
    query_str_list = query_str.split(" ")
    simply_corpus = simply(corpus)
    bm25Model = bm25.BM25(simply_corpus)
    average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())
    scores = bm25Model.get_scores(query_str_list, average_idf)
    position = scores.index(max(scores))
    aim_sentence = documentation[documentation_id]["text"][position]
    return aim_sentence


def BM25(question_input):
    documentation_id=question_input["docid"]
    sentence = []
    corpus = []
    temp=[]
    temp_fini=[]
    for word in documentation[documentation_id]["text"]:
        sentence.append([word])
    for i in sentence:
        for k in i:
            word_list = k.split(" ")
        corpus.append(word_list)
        word_list = []

    query_str = question_input["question"]
    query_str_list = query_str.split(" ")
    simply_corpus = simply(corpus)
    bm25Model = bm25.BM25(simply_corpus)
    average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())
    scores = bm25Model.get_scores(query_str_list, average_idf)
    position = scores.index(max(scores))
    aim_sentence = documentation[documentation_id]["text"][position]
    aim_sentence_list=aim_sentence.split(".")
    for a in aim_sentence_list:
        temp_word=a.split(" ")
        for k in temp_word:
            temp.append(k)
        temp_fini.append(temp)
        temp=[]
    tmp_fini_simply=simply(temp_fini)
    bm25Model = bm25.BM25(tmp_fini_simply)
    average_idf = sum(map(lambda k: float(bm25Model.idf[k]), bm25Model.idf.keys())) / len(bm25Model.idf.keys())
    scores = bm25Model.get_scores(query_str_list, average_idf)
    position = scores.index(max(scores))
    aim_sentence =aim_sentence_list[position]
#    print("aim_sentence",aim_sentence)
    return aim_sentence


def find_aim_sentence_first(Q):
    num = []
    name = []
    org = []
    pos = []
    noun = []
    ner_question = tree2conlltags(ne_chunk(pos_tag(word_tokenize(Q['question']))))

    for word in ner_question:
        if word[1] == 'CD':
            num.append(word[0])
        elif word[2] == 'B-PERSON' or word[2] == 'I-PERSON':
            name.append(word[0])
        elif word[2] == 'B-ORGANIZATION' or word[2] == 'I-ORGANIZATION':
            org.append(word[0])
        elif word[2] =='B-GPE' or word[2] == 'I-GPE' or word[2] == 'B-LOCATION' or word[2] == 'I-LOCATION':
            pos.append(word[0])
#        if word[1] == "NN" or word[1] == "NNP":
        if word[1]=="NN" or word[1] == "NNP":
            noun.append(word[0])

    ture_sentence = []
    aim_sentence = BM25_pragrah(Q)
    all_sent = sent_tokenize(aim_sentence)


# rank question
    Q_word = Q['question'].split()
    rank_list = ['rank', 'ranking', 'ranked']
    for rank in rank_list:
        for word in Q_word:
            if rank == word:
                for sent in all_sent:
    # ordinal(ranking) must in the answer
                    nlp = spacy.load('en_core_web_sm')
                    sent_parse = nlp(sent)
                    rank_flag = False
                    for word in sent_parse.ents:
                        if word.label_ == 'ORDINAL':
                            rank_flag = True
                            break
                    if rank_flag == False:
                        continue
                    else:
                        if len(num) > 0:
                            for n in num:
                                if n not in sent:
                                    break
                        elif len(name) > 0:
                            for n in name:
                                if n not in sent:
                                    break
                        elif len(org) > 0:
                            for o in org:
                                if o not in sent:
                                    break
                        elif len(pos) > 0:
                            for p in pos:
                                if p not in sent:
                                        break
                    i = 0
                    for n in noun:
                        if n in sent:
                            i += 1
                    if i >= len(noun)*0.5:
                        ture_sentence = sent
                        # break
                        return ture_sentence

# percentage question
    for percentage_question in percentage_question_list:
        for sent in all_sent:
            if percentage_question in sent:
                nlp = spacy.load('en_core_web_sm')
                sent_parse = nlp(sent)
                percentage_flag = False
                for word in sent_parse.ents:
                    if word.label_ == 'PERCENT':
                        percentage_flag = True
                        break
                if percentage_flag == False:
                    continue
                else:
                    if len(num) > 0:
                        for n in num:
                            if n not in sent:
                                break
                    elif len(name) > 0:
                        for n in name:
                            if n not in sent:
                                break
                    elif len(org) > 0:
                        for o in org:
                            if o not in sent:
                                break
                    elif len(pos) > 0:
                        for p in pos:
                            if p not in sent:
                                    break
                i = 0
                for n in noun:
                    if n in sent:
                        i += 1
                if i >= len(noun)*0.5:
                    ture_sentence = sent
                    # break
                    return ture_sentence

# time question
    time_question_list = []
    for word in data_question_list:
        time_question_list.append(word)
    for word in year_question_list:
        time_question_list.append(word)
    for time_question in time_question_list:
        for sent in all_sent:
            if time_question in sent:
                nlp = spacy.load('en_core_web_sm')
                sent_parse = nlp(sent)
                time_flag = False
                for word in sent_parse.ents:
                    if word.label_ == 'DATE' or word.label_ == 'TIME':
                        time_flag = True
                        break
                if time_flag == False:
                    continue
                else:
                    if len(num) > 0:
                        for n in num:
                            if n not in sent:
                                break
                    elif len(name) > 0:
                        for n in name:
                            if n not in sent:
                                break
                    elif len(org) > 0:
                        for o in org:
                            if o not in sent:
                                break
                    elif len(pos) > 0:
                        for p in pos:
                            if p not in sent:
                                    break
                i = 0
                for n in noun:
                    if n in sent:
                        i += 1
                if i >= len(noun)*0.5:
                    ture_sentence = sent
                    # break
                    return ture_sentence

# number question
    for number_question in number_question_list:
        for sent in all_sent:
            if number_question in sent:
                nlp = spacy.load('en_core_web_sm')
                sent_parse = nlp(sent)
                number_flag = False
                for word in sent_parse.ents:
                    if word.label_ == 'QUANTITY' or word.label_ == 'CARDINAL':
                        number_flag = True
                        break
                if number_flag == False:
                    continue
                else:
                    if len(num) > 0:
                        for n in num:
                            if n not in sent:
                                break
                    elif len(name) > 0:
                        for n in name:
                            if n not in sent:
                                break
                    elif len(org) > 0:
                        for o in org:
                            if o not in sent:
                                break
                    elif len(pos) > 0:
                        for p in pos:
                            if p not in sent:
                                    break
                i = 0
                for n in noun:
                    if n in sent:
                        i += 1
                if i >= len(noun)*0.5:
                    ture_sentence = sent
                    # break
                    return ture_sentence

    return ture_sentence


def find_aim_sentence(question_input):
    aim_sentence=[]
    query_str = question_input["question"]
    if re.search("in [0-9]{4}",question_input["question"]) or re.search("In [0-9]{4}",question_input["question"]):
        data_list_aim=find_aim_sentence_time(question_input)
        if data_list_aim!=[]:
           aim_sentence=data_list_aim
    if aim_sentence==[]:
        data_list_aim=find_aim_sentence_first(question_input)
        if data_list_aim!=[]:
            aim_sentence=data_list_aim
    if aim_sentence==[]:
        data_list_aim=find_aim_sentence_special(question_input)
        if data_list_aim!=[]:
            aim_sentence=data_list_aim
    if aim_sentence==[]:
        aim_sentence=BM25(question_input)
    if aim_sentence==None:
        return []
#    print("aim_sentence",aim_sentence)
    for who in person_question_list:
        if who in query_str:
            data_list=get_name(aim_sentence)
            return data_list


    for year in year_question_list:
        if year in query_str:
            data_list=get_year(aim_sentence)
            return data_list

    for data in data_question_list:
        if data in query_str:
            data_list=get_date(aim_sentence)
            return data_list

    for percentage in percentage_question_list:
        if percentage in query_str:
            data_list=get_percentage(aim_sentence)
            return data_list

    for money in money_question_list:
        if money in query_str:
            data_list=get_money(aim_sentence)
            return data_list


    for where in Loctaion_question_list:
        if where in query_str:
            data_list=get_location(aim_sentence)
            return data_list


    for number in number_question_list:
        if number in query_str:
            data_list=get_number(aim_sentence)
            return data_list

    data_list=whatQuestion(aim_sentence,query_str)
    return data_list
count=0
#for i in testing:
#    print(count,i)
#    count=count+1
#print(question[3094])
#print(find_aim_sentence(question[3094]))
fileHeader=["id","answer"]
csvFile=open("project_test10.csv","w")
writer=csv.writer(csvFile)
writer.writerow(fileHeader)
count=0
aim_answer=""
finin_list=list()
for i in testing:
    aim_data=list(set(find_aim_sentence(i)))
    if len(aim_data)==1:
        aim_answer=aim_data[0].lower()
    else:
       for k in range(len(aim_data)):
            if k < len(aim_data)-1:
                aim_answer=aim_data[k].lower()+" "+aim_answer
            if k==len(aim_data)-1:
                aim_answer=aim_answer+aim_data[k].lower()
    finin_list.append((str(count),aim_answer))
    count=count+1
    aim_answer=""
    print(count)
writer.writerows(finin_list)
csvFile.close()

#print(find_aim_sentence(aim_sentecen))
