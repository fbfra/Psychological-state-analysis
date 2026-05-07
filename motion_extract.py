def extr_moti_td(story_id, td, story_set): # 提取时故事id应在ids_test/ids_dev中
    moti=[]
    all_info=td[td.storyid==story_id]
    story=story_set[story_set.storyid==story_id]
    # 提取故事中的人物，数组类型，元素为字符串
    chars=set(all_info.char.values)
    for cha in chars:
        motiv=[]
        masl=[]
        reis=[]
        sents=[]
        # 每个人物出现的句子行
        lines=all_info[all_info.char==cha]
        li=set(lines.linenum.values)
        li_num=[] # 记录有动机的行
        for i in li:
            # 提取只有此行的条目
            li_i=lines[lines.linenum==i]
            for t in range(li_i.shape[0]):   # 对此行的每一种注释
                if li_i.iloc[t].action=='yes' and li_i.iloc[t].maslow[2:-2]!='none':
                    motiv.extend(li_i.iloc[t].motivation[2:-2].split('", "'))
                    masl.extend(li_i.iloc[t].maslow[2:-2].split('", "'))
                    reis.extend(li_i.iloc[t].reiss[2:-2].split('", "'))
                    li_num.append(i)
        motiv=[m for m in list(set(motiv)) if m!=''] # 去掉重复的情绪描述
        masl=[ ma for ma in list(set(masl)) if ma!='']
        reis=[r for r in list(set(reis)) if r!='']
        if len(li_num)!=0:
            max_line=max(li_num)
            for j in range(max_line):
                sents.append(story['sentence'+str(j+1)].values[0])
            moti.append((cha,motiv,masl,reis,sents))
    return moti

for id_test in ids_test:
    id_con=extr_moti_td(id_test, sc_test_moti, story_test)
    for item in id_con:
        for mas in item[2]:
            if mas in maslow:
                mas_text[mas].append((item[0], item[4]))
    for item in id_con:
        for rei in item[3]:
            if rei in reiss:
                reis_text[rei].append((item[0], item[4]))

def extract_moti(string):  # 每一行
    string=string.split(',')
    for i in range(len(string)):
        mo=''
        for n in range(len(string[i])):
            if string[i][n].isalpha():
                mo+=string[i][n]
        string[i]=mo
    return string

# 定义一个函数，输入为每个标签读取后的json文件，输出为(故事id, 句子联合文本)的元组列表
def char_merge(read_file):
    label_relat=[]
    ids=set(read_file[0].values)
    for id in ids:
        subs=read_file[read_file[0].values==id]
        seen = set()
        uni = []
        for i in range(len(subs[2].values)):
            for sent in subs[2].values[i]:
                if sent not in seen:
                    seen.add(sent)
                    uni.append(sent)
        con=' '.join(uni)
        label_relat.append((id, con))
    return label_relat

