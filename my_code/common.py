import random
import matplotlib.pyplot as plt


def test_info(avg_insert_mem, avg_delete_mem, avg_search_mem, avg_insert_hash, avg_delete_hash, avg_search_hash, avg_insert_time):
    print(f'AVG mem_cnt on insert = {avg_insert_mem}')
    print(f'AVG hash_cnt on insert = {avg_insert_hash}')
    print(f'AVG TIME on insert = {avg_insert_time}\n')

    print(f'AVG mem_cnt on search = {avg_search_mem}')
    print(f'AVG hash_cnt on search = {avg_search_hash}\n')

    print(f'AVG mem_cnt on delete = {avg_delete_mem}')
    print(f'AVG hash_cnt on delete = {avg_delete_hash}\n')




def draw(avg_insert_mem, avg_delete_mem, avg_search_mem, avg_insert_hash, avg_delete_hash, avg_search_hash, avg_insert_time, name):
    # 1. Обращения к памяти
    plt.figure(figsize=(6, 4))
    plt.bar(['Вставка', 'Удаление', 'Поиск'], [avg_insert_mem, avg_delete_mem, avg_search_mem], color=['skyblue', 'salmon', 'pink'], width=0.4)
    plt.title('Среднее число обращений к памяти')
    plt.ylabel('Число обращений')
    plt.grid(True, linestyle='--', alpha=0.5)
    for i, v in enumerate([avg_insert_mem, avg_delete_mem, avg_search_mem]):
        plt.text(i, v + 0.5, f'{v:.2f}', ha='center')
    plt.tight_layout()
    max_val = max(avg_insert_mem, avg_delete_mem, avg_search_mem)
    plt.ylim(0, max_val * 1.2)
    plt.savefig(f'{name}_memory.png')
    plt.show()

    # 2. Вызовы хеш-функции
    plt.figure(figsize=(6, 4))
    plt.bar(['Вставка', 'Удаление', 'Поиск'], [avg_insert_hash, avg_delete_hash, avg_search_hash], color=['skyblue', 'salmon', 'pink'], width=0.4)
    plt.title('Среднее число вызовов хеш-функции')
    plt.ylabel('Число вызовов')
    plt.grid(True, linestyle='--', alpha=0.5)
    for i, v in enumerate([avg_insert_hash, avg_delete_hash, avg_search_hash]):
        plt.text(i, v + 0.5, f'{v:.2f}', ha='center')
    plt.tight_layout()
    max_val = max(avg_insert_hash, avg_delete_hash, avg_search_hash)
    plt.ylim(0, max_val * 1.2)
    plt.savefig(f'{name}_hash.png')
    plt.show()

    # 3. Время вставки
    plt.figure(figsize=(6, 4))
    plt.bar(['Вставка'], [avg_insert_time], color='skyblue', width=0.01)
    plt.title('Среднее время выполнения вставки')
    plt.ylabel('Время (сек)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.text(0, avg_insert_time + 0.0001, f'{avg_insert_time:.6f}', ha='center')
    plt.tight_layout()
    max_val = max([avg_insert_time])
    plt.ylim(0, max_val * 1.2)
    plt.savefig(f'{name}_time.png')
    plt.show()

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