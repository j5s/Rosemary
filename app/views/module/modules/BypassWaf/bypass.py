# -*- coding:utf-8 -*-
import random

all_chunklen = [] #用于存放所有的长度信息
all_data = [] #用于存放所有正常数据
all_garbages_datas = [] #用于存放垃圾数据
All_data_remark_garb = [] #用于存放最终插入垃圾数据后的结果


def random_split(string,count):
    length = len(string)
    num = range(1, length+1)  # 生成数字1~长度+1的列表，内容是不重复的
    nums = random.sample(num, count)  # 从上面的列表中随机选取count个不同数字
    nums.sort(reverse=False) # reverse=False表示升序，True表示降序

    start_point = 0 #初始化第一次读取的起始位为0
    for i in range(count): #因为range取的是0~count-1，所以这里count要+1
        chunk_len = str(nums[i]-start_point)
        all_chunklen.append(chunk_len)
        data = string[start_point:nums[i]]
        all_data.append(data)
        start_point = nums[i] #作为下一次读取的起始位
        #print(i)
        if i == count-1:
            chunk_len = str(length - start_point)
            all_chunklen.append(chunk_len)
            #print(chunk_len)
            data = string[start_point:length]
            all_data.append(data)
            #print(data)
            break



def garbage_data(min_size,max_size,count):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*(),./\\|{}[] :;~`'
    n = 0
    #for data_len in random.randint(min_size,max_size+1): #生成每次要插入的垃圾数据长度
    while n <= count:
        data_len = random.randint(min_size,max_size+1)
        characters = random.sample(alphabet, data_len)
        characters_toStr = ';' + ''.join(characters)
        n+=1
        garbages_data = characters_toStr
        all_garbages_datas.append(garbages_data)



def create_rs_data(string): #通过拼接三个全局列表中的内容生成最后结果
    count = 3
    print(string)
    random_split(string,count)
    garbage_data(1,5,count)
    s = ""
    for i in range(count+1):
        data = str(all_chunklen[i]) + str(all_garbages_datas[i]).strip('\n') + '\n' + str(all_data[i])
        s = s + data
    return s


