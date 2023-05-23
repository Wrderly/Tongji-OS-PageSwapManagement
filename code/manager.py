import queue


def managerLog(code_num, current_code_id, need_swap, swap_out_task_page_id, swap_in_task_page_id,
               swap_memory_page_id):
    print('第' + str(code_num) + '条指令 ' +
          ' 指令地址' + str(current_code_id).ljust(3) +
          (' 需要换页 ' if need_swap else ' 不需要换页 ').ljust(12) +
          ' 换出页' + (str(swap_out_task_page_id) if swap_out_task_page_id != -1 else ' - ').ljust(3) +
          ' 换入页' + (str(swap_in_task_page_id) if swap_in_task_page_id != -1 else ' - ').ljust(3) +
          ' 被换页内存页' + (str(swap_memory_page_id) if swap_memory_page_id != -1 else ' - ').ljust(3))


class MyManager:
    def __init__(self, page_size, algo):
        self.task_memory_page_amount = 4  # 分配给任务的页面数
        self.page_size = page_size  # 页面尺寸
        self.task_page = [None for i in range(self.task_memory_page_amount)]  # 分配的页面 记录页面号
        self.code_num = 0  # 记录执行到第几条代码
        self.algo = algo  # 记录设定的管理器的算法

        if self.algo == 'FIFO':  # 根据不同的算法配置不同的参数
            self.page_allocate_queue = queue.Queue()  # 记录页面分配顺序
        elif self.algo == 'LRU':
            self.unused_time = [None for i in range(self.task_memory_page_amount)]  # 记录页面未被使用的时间
            self.page_allocated_amount = 0

    def runTask(self, task):
        if self.algo == 'FIFO':
            return self.runTaskByFIFO(task)
        elif self.algo == 'LRU':
            return self.runTaskByLRU(task)

    def runTaskByFIFO(self, task):
        # 从task中获取当前要执行的代码的信息
        current_code_id, memory_page_for_code, code_page_id = task.getCurrentCodeId()
        # 初始化log
        log1, log2, log3, log4, log5, log6 = 0, 0, False, -1, -1, -1
        if memory_page_for_code != -1:  # 在内存中
            log3, log4, log6 = False, -1, memory_page_for_code
        else:  # 不在内存中
            if self.page_allocate_queue.qsize() < self.task_memory_page_amount:  # 内存没有分配满
                for i in range(self.task_memory_page_amount):
                    if self.task_page[i] is None:  # 找到空位置
                        self.task_page[i] = code_page_id
                        task.pcb.page_table[code_page_id] = i
                        self.page_allocate_queue.put(i)
                        log3, log4, log6 = True, -1, i
                        break
            else:  # 内存被分配满 进行页面调换
                dst_memory_page_id = self.page_allocate_queue.get()  # 从队列中取出最早分配的页序号
                old_page = self.task_page[dst_memory_page_id]
                self.task_page[dst_memory_page_id] = code_page_id
                task.pcb.page_table[old_page] = -1
                task.pcb.page_table[code_page_id] = dst_memory_page_id
                self.page_allocate_queue.put(dst_memory_page_id)  # 新分配的页序号插入队尾
                log3, log4, log6 = True, old_page, dst_memory_page_id
        log1, log2, log5 = self.code_num, current_code_id, code_page_id
        # managerLog(log1, log2, log3, log4, log5, log6)

        self.code_num = self.code_num + 1
        return log1, log2, log3, log4, log5, log6

    def add_unused_time(self):
        for i in range(self.task_memory_page_amount):
            if self.unused_time[i] is not None:
                self.unused_time[i] = self.unused_time[i] + 1

    def runTaskByLRU(self, task):
        # 从task中获取当前要执行的代码的信息
        current_code_id, memory_page_for_code, code_page_id = task.getCurrentCodeId()
        # 初始化log
        log1, log2, log3, log4, log5, log6 = 0, 0, False, -1, -1, -1
        if memory_page_for_code != -1:  # 在内存中
            self.add_unused_time()
            self.unused_time[memory_page_for_code] = 0
            log3, log4, log6 = False, -1, memory_page_for_code
        else:  # 不在内存中
            if self.page_allocated_amount < self.task_memory_page_amount:  # 内存没有分配满
                for i in range(self.task_memory_page_amount):
                    if self.task_page[i] is None:  # 找到空位置
                        self.task_page[i] = code_page_id
                        task.pcb.page_table[code_page_id] = i
                        self.page_allocated_amount = self.page_allocated_amount + 1
                        self.add_unused_time()
                        self.unused_time[i] = 0
                        log3, log4, log6 = True, -1, i
                        break
            else:  # 内存被分配满 进行页面调换
                dst_memory_page_id = self.unused_time.index(max(self.unused_time))  # 从队列中取出最久未使用的页序号
                old_page = self.task_page[dst_memory_page_id]
                self.task_page[dst_memory_page_id] = code_page_id
                task.pcb.page_table[old_page] = -1
                task.pcb.page_table[code_page_id] = dst_memory_page_id
                self.add_unused_time()
                self.unused_time[dst_memory_page_id] = 0
                log3, log4, log6 = True, old_page, dst_memory_page_id
        log1, log2, log5 = self.code_num, current_code_id, code_page_id
        # managerLog(log1, log2, log3, log4, log5, log6)

        self.code_num = self.code_num + 1
        return log1, log2, log3, log4, log5, log6
