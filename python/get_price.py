import pandas as pd
import time
agg_csv = pd.read_csv('STXUSDT-aggTrades-2022-10.csv')
#print(agg_csv.head())
#print(agg_csv[:3])
start = 0
end = len(agg_csv)
dt_start_time = "2022-10-02 07:00:00"
timeArray = time.strptime(dt_start_time,"%Y-%m-%d %H:%M:%S")
start_stamp = time.mktime(timeArray)

#print(timestamp)
hour = 3600
minute = 60
# for j in range(0,10):
#     start_stamp = start_stamp + j * hour * 24
#     end_stamp = start_stamp + hour * 1
#     flag=1
#             #print(type(datatime),datatime)
#     timeArray = time.localtime(start_stamp)
#     view_time = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
#     print(view_time)
day_count = 0
end_stamp = start_stamp + hour * 1
flag = 1
start_price = 0
target_price = 0
target_flag = 0
count = 0
low_flag  = 0
all_count = 0
for i in range(0,end,1):
    data = agg_csv[i:i+1].to_numpy()
    datatime = data[0][5]/1000
    timeArray = time.localtime(datatime)
    view_time = time.strftime("%Y-%m-%d %H:%M:%S",timeArray)
    if datatime >= start_stamp and flag==1:
        print("")
        print("")
        print("start ",view_time)
        flag=0
        start_price = data[0][1]
        target_price = data[0][1] + data[0][1] * 0.01
        target_flag = 1
        start_stamp = start_stamp + hour * 24
        all_count += 1
        print("start_time,本日起始时间",view_time,data)
        low_price = data[0][1] + data[0][1] * 0.01

    if  datatime <= start_stamp and data[0][1] >= target_price and target_flag == 1:
        print("arrive target_price",view_time,data)
        target_flag = 0
        count += 1


    
    if datatime >= end_stamp:
        flag = 1
        end_stamp = start_stamp + hour*1
        end_price = data[0][1]
        print("end_time 本日终止时间",data,end_price-start_price)
        #target_flag = 1
        #break

print(all_count)
print(count)

#time.strftime
