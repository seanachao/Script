#### 从excel中读取数据每一个sheet并处理

import pandas as pd

import pandas as pd


data = []
for i in range(0,5):
    data.append(pd.read_excel('D:\\excel\\tmp.xlsx',sheet_name=i))

def select_data(content,yearp,total_res): 
    
    for i in range(0,len(content)):
        line_data = content[i]
        if yearp[i] !=2016:
            continue
        if '、' in content:
            words = line_data.split('、')
        else:
            words = line_data.split('，')

        for _ in words:
            if not _:
                continue
            if _ in total_res:
                total_res.update({_:total_res[_]+1})
            else:
                total_res.update({_:1})
    
    return total_res


contents = []
total_res = {}
years = []
print(len(data))
tmp_res = {}
for i in range(0,len(data)):
    tmp_res = select_data(data[i]['主要关键词'],data[i]['年份'],total_res)
    total_res.update(tmp_res)

print (total_res)
df = pd.Series(total_res)

df_df = pd.DataFrame(df)

df_df.to_excel('D:\\excel\\output.xlsx')



