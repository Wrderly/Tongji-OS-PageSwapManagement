import random


class Pcb:
    def __init__(self, page_size, code_amount):
        self.task_page_table_size = code_amount // page_size
        if code_amount % page_size != 0:
            self.task_page_table_size = self.task_page_table_size + 1
        self.page_table = [-1 for i in range(self.task_page_table_size)]  # 记录程序的每一页在内存中的哪一页 值为-1则不在内存中


class Task:
    def __init__(self, page_size, code_amount):
        self.code_amount = code_amount  # 代码数量
        self.page_size = page_size  # 页尺寸
        self.pcb = Pcb(page_size, code_amount)  # 记录任务信息
        self.current_code_id = random.randint(0, self.code_amount - 1)  # 当前代码序号
        self.state = 0  # 状态，用于生成下一条代码的序号

    def getCurrentCodeId(self):
        tmp_code_id = self.current_code_id
        if self.state == 0:
            self.current_code_id = (self.current_code_id + 1) % self.code_amount  # 顺序执行
            self.state = 1
        elif self.state == 1:
            self.current_code_id = random.randint(0, max(self.current_code_id - 1, 0))  # 在前面的代码中随机取
            self.state = 2
        elif self.state == 2:
            self.current_code_id = (self.current_code_id + 1) % self.code_amount  # 顺序执行
            self.state = 3
        elif self.state == 3:
            self.current_code_id = random.randint(min(self.current_code_id + 1, self.code_amount - 1), self.code_amount - 1)  # 在后面的代码中随机取
            self.state = 0
        return tmp_code_id, self.pcb.page_table[tmp_code_id // self.page_size], tmp_code_id // self.page_size
