"""Здесь будут проводиться тестирования Отелло хеширования при загрузке таблицы в 90%"""
"""Сравнительное тестирование времени работы операции поиска"""

import json
import pog
import random
import time
from common import get_keys, generate_mac, generate_vlan, generate_kv, draw, test_info
import numpy as np


def test_correct(oth, json_dict, keys):
    cnt = 0
    for i in range(len(json_dict)):
       key = keys[i]
       ans = oth.search(key)[0]

       #print(ans,json_dict[key], key)
       if str(json_dict[key]) == str(ans):
              cnt += 1

    return cnt


with open('mac_vlan_mapping.json', 'r') as JSON:
    json_dict = json.load(JSON)

keys, values = get_keys(json_dict)
pg = pog.POG()
pg.construct(json_dict)

'''Вычисление, сколько элементов надо добавить для текущих размеров Отелло, чтобы загрузка стала определенной'''
max_load = pg.group[0].ma
n = len(json_dict)
print(f'max_load = {max_load}, current_load = {n}')
load = 0.5 
# Добавляем недостающее число правил, чтобы загрузка каждой доли графа стала фиксированной
for i in range(int((max_load * load - n))):
    new_k, new_v = generate_kv()
    info = pg.insert(json_dict, new_k, new_v)
    #print(f'{i}/{int(max_load * 0.9 - n)} ВСТАВКА. Кол-во обращений к памяти = {info.memory}')
    json_dict[new_k] = new_v

print(f'Текущая загрузка доли графа: {len(json_dict)} / {max_load}')
keys, values = get_keys(json_dict)
cnt = test_correct(pg, json_dict, keys)
print(f'Correct is {cnt} of {len(json_dict)}')


"""Тестирование среднего числа обращений к памяти и вызовов хеш-функции на операции ВСТАВКИ при 90% загрузке"""
"""Тестирование среднего числа обращений к памяти и вызовов хеш-функции на операции УДАЛЕНИЕ при 90% загрузке"""
insert_memory_cnt = []
insert_hash_cnt = []
insert_time = []

delete_mem_cnt = []
delete_hash_cnt = []
for _ in range(100):
    new_k, new_v = generate_kv()

    start_t = time.time()
    info_ins = pg.insert(json_dict, new_k, new_v)
    finish_t = time.time()
    insert_memory_cnt.append(info_ins.memory)
    insert_hash_cnt.append(info_ins.hash)
    insert_time.append(finish_t - start_t)

    info_del = pg.delete(new_k)
    delete_mem_cnt.append(info_del.memory)
    delete_hash_cnt.append(info_del.hash)


"""Тестирование среднего числа обращений к памяти и вызовов хеш-функции на операции ПОИСКА при 90% загрузке"""
search_memory_cnt = []
search_hash_cnt = []
for i in range(len(json_dict)):
    key = keys[i]
    ans, info = pg.search(key)
    search_memory_cnt.append(info.memory)
    search_hash_cnt.append(info.hash)
    #print(ans,json_dict[key], key)
    if str(json_dict[key]) == str(ans):
        cnt += 1

avg_insert_mem = sum(insert_memory_cnt) / len(insert_memory_cnt)
avg_delete_mem = sum(delete_mem_cnt) / len(delete_mem_cnt)
avg_search_mem = sum(search_memory_cnt) / len(search_memory_cnt)

avg_insert_hash = sum(insert_hash_cnt) / len(insert_hash_cnt)
avg_delete_hash = sum(delete_hash_cnt) / len(delete_hash_cnt)
avg_search_hash = sum(search_hash_cnt) / len(search_hash_cnt)

avg_insert_time = sum(insert_time) / len(insert_time)


test_info(avg_insert_mem, avg_delete_mem, avg_search_mem, avg_insert_hash, avg_delete_hash, avg_search_hash, avg_insert_time)
draw(avg_insert_mem, avg_delete_mem, avg_search_mem, avg_insert_hash, avg_delete_hash, avg_search_hash, avg_insert_time, name='oth')



keys, values = get_keys(json_dict)
cnt = test_correct(pg, json_dict, keys)
print(f'Correct is {cnt} of {len(json_dict)}')




