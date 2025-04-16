"""Здесь будут проводиться тестирования Отелло хеширования при загрузке таблицы в 90%"""
"""Сравнительное тестирование времени работы операции поиска"""

import json
import pog
import random

def get_keys(json_dict):
    keys = []
    values = []
    for k, v in json_dict.items():
       keys.append(k)
       values.append(v)
    return keys, values


def generate_mac():
    """Генерирует случайный MAC-адрес."""
    return ':'.join(f"{random.randint(0, 255):02X}" for _ in range(6))


def generate_vlan():
    """Генерирует случайный VLAN ID (от 1 до 4095)."""
    return random.randint(1, 4095)


def generate_kv():
    mac = generate_mac()
    vlan = generate_vlan()
    key = f"{mac}-{vlan}"
    value = str(random.randint(0, 30))  # Порт
    return key, value


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

'''Вычисление, сколько элементов надо добавить для текущих размеров Отелло, чтобы загрузка стала 90'''
max_load = pg.group[0].ma
n = len(json_dict)
print(f'max_load = {max_load}, current_load = {n}')
# Добавляем недостающее число правил, чтобы загрузка каждой доли графа стала 90%
for i in range(int((max_load * 0.9 - n))):
    new_k, new_v = generate_kv()
    info = pg.insert(json_dict, new_k, new_v)
    print(f'{i}/{int(max_load * 0.9 - n)} ВСТАВКА. Кол-во обращений к памяти = {info.memory}')
    json_dict[new_k] = new_v

print(f'Текущая загрузка доли графа: {len(json_dict)} / {max_load}')
keys, values = get_keys(json_dict)
cnt = test_correct(pg, json_dict, keys)
print(f'Correct is {cnt} of {len(json_dict)}')


"""Тестирование среднего числа обращений к памяти на операции ВСТАВКИ при 90% загрузке"""
"""Тестирование среднего числа обращений к памяти и вызовов хеш-функции на операции УДАЛЕНИЕ при 90% загрузке"""
insert_memory_cnt = []
delete_mem_cnt = []
delete_hash_cnt = []
for _ in range(100):
    new_k, new_v = generate_kv()
    info_ins = pg.insert(json_dict, new_k, new_v)
    insert_memory_cnt.append(info_ins.memory)

    info_del = pg.delete(new_k)
    delete_mem_cnt.append(info_del.memory)
    delete_hash_cnt.append(info_del.hash)
print(f'AVG mem_cnt on insert = {sum(insert_memory_cnt) / len(insert_memory_cnt)}')
print(f'AVG mem_cnt on delete = {sum(delete_mem_cnt) / len(delete_mem_cnt)}')
print(f'AVG hash_cnt on delete = {sum(delete_hash_cnt) / len(delete_hash_cnt)}')


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
print(f'AVG mem_cnt on search = {sum(search_memory_cnt) / len(search_memory_cnt)}')
print(f'AVG hash_cnt on search = {sum(search_hash_cnt) / len(search_hash_cnt)}')




