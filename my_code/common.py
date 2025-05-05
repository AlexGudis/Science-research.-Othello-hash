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
    value = str(random.randint(0, 5))  # Порт
    return key, value


class Info():
    def __init__(self, type='', records = 0, key_inc = False, memory = 0, hash = 0, failed = 0, contruct_cnt = 0):
        self.type = type
        self.records = records
        self.key_inc = key_inc
        self.memory = memory   # число доступов к памяти
        self.hash = hash   # число вычислений хеш-функций
        self.failed = failed
        self.contruct_cnt = contruct_cnt   # число перестроений структуры для операции insert в Отелло