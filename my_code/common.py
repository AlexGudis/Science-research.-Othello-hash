class Info():
    def __init__(self, type='', records = 0, key_inc = False, memory = 0, hash = 0, failed = 0, contruct_cnt = 0):
        self.type = type
        self.records = records
        self.key_inc = key_inc
        self.memory = memory   # число доступов к памяти
        self.hash = hash   # число вычислений хеш-функций
        self.failed = failed
        self.contruct_cnt = contruct_cnt   # число перестроений структуры для операции insert в Отелло