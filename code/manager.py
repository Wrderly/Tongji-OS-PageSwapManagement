import queue


class MyManager:
    def __init__(self, page_size, algo):
        self.task_memory_page_amount = 4  # 分配给任务的页面数
        self.page_size = page_size  # 页面尺寸
        self.task_page = [None for i in range(self.task_memory_page_amount)]  # 分配的页面 记录页面号
        self.code_num = 0  # 记录执行到第几条代码
        self.algo = algo  # 记录设定的管理器的算法
        self.page_allocated_amount = 0

        if self.algo == 'FIFO':  # 根据不同的算法配置不同的参数
            self.page_allocate_queue = queue.Queue()  # 记录页面分配顺序
        elif self.algo == 'LRU':
            self.unused_time = [None for i in range(self.task_memory_page_amount)]  # 记录页面未被使用的时间

    def pageSwap(self, dst_memory_page_id, code_page_id, task):  # 页面调换
        old_page = self.task_page[dst_memory_page_id]  # 该模拟内存页上存放的旧作业页
        self.task_page[dst_memory_page_id] = code_page_id  # 写入新作业页
        task.pcb.page_table[old_page] = -1  # 旧作业页的页表置-1
        task.pcb.page_table[code_page_id] = dst_memory_page_id  # 新作业页的页表置模拟内存页号
        return old_page

    def allocateEmptyPage(self, empty_page_id, code_page_id, task):  # 分配空页面
        self.task_page[empty_page_id] = code_page_id
        task.pcb.page_table[code_page_id] = empty_page_id
        self.page_allocated_amount += 1

    def add_unused_time(self, used_page_id):  # 用于LRU算法，增加界面的“未被使用时间”
        for i in range(self.task_memory_page_amount):
            if self.unused_time[i] is not None:
                self.unused_time[i] += 1  # 增加界面的“未被使用时间”
        self.unused_time[used_page_id] = 0  # 被使用的界面则清空“未被使用时间”

    def runTask(self, task):
        if self.algo == 'FIFO':
            return self.runTaskByFIFO(task)
        elif self.algo == 'LRU':
            return self.runTaskByLRU(task)

    def runTaskByFIFO(self, task):
        # 从task中获取当前要执行的代码的信息
        current_code_id, memory_page_for_code, code_page_id = task.getCurrentCodeId()
        # 初始化log 用于记录可视化界面所需信息
        code_num_log, cur_code_log, need_page_log, old_page_log, code_page_log, memory_page_log = 0, 0, False, -1, -1, -1
        if memory_page_for_code != -1:  # 在内存中
            need_page_log, old_page_log, memory_page_log = False, -1, memory_page_for_code  # 记录可视化界面所需信息
        else:  # 不在内存中
            if self.page_allocated_amount < self.task_memory_page_amount:  # 内存没有分配满
                for i in range(self.task_memory_page_amount):
                    if self.task_page[i] is None:  # 找到空位置
                        self.allocateEmptyPage(i, code_page_id, task)  # 分配空的模拟内存页面
                        self.page_allocate_queue.put(i)  # 插入FIFO算法队列
                        need_page_log, old_page_log, memory_page_log = True, -1, i  # 记录可视化界面所需信息
                        break
            else:  # 内存被分配满 进行页面调换
                dst_memory_page_id = self.page_allocate_queue.get()  # 从队列中取出最早分配的页序号
                old_page = self.pageSwap(dst_memory_page_id, code_page_id, task)  # 页面调换
                self.page_allocate_queue.put(dst_memory_page_id)  # 新分配的页序号插入队尾
                need_page_log, old_page_log, memory_page_log = True, old_page, dst_memory_page_id  # 记录可视化界面所需信息
        code_num_log, cur_code_log, code_page_log = self.code_num, current_code_id, code_page_id  # 记录可视化界面所需信息
        self.code_num += 1
        return code_num_log, cur_code_log, need_page_log, old_page_log, code_page_log, memory_page_log

    def runTaskByLRU(self, task):
        # 从task中获取当前要执行的代码的信息
        current_code_id, memory_page_for_code, code_page_id = task.getCurrentCodeId()
        # 初始化log 用于记录可视化界面所需信息
        code_num_log, cur_code_log, need_page_log, old_page_log, code_page_log, memory_page_log = 0, 0, False, -1, -1, -1
        if memory_page_for_code != -1:  # 在内存中
            self.add_unused_time(used_page_id=memory_page_for_code)  #
            need_page_log, old_page_log, memory_page_log = False, -1, memory_page_for_code  # 记录可视化界面所需信息
        else:  # 不在内存中
            if self.page_allocated_amount < self.task_memory_page_amount:  # 内存没有分配满
                for i in range(self.task_memory_page_amount):
                    if self.task_page[i] is None:  # 找到空位置
                        self.allocateEmptyPage(i, code_page_id, task)  # 分配空的模拟内存页面
                        self.add_unused_time(used_page_id=i)  # 更新LRU算法记录的未使用时间
                        need_page_log, old_page_log, memory_page_log = True, -1, i  # 记录可视化界面所需信息
                        break
            else:  # 内存被分配满 进行页面调换
                dst_memory_page_id = self.unused_time.index(max(self.unused_time))  # 从队列中取出最久未使用的页序号
                old_page = self.pageSwap(dst_memory_page_id, code_page_id, task)  # 页面调换
                self.add_unused_time(used_page_id=dst_memory_page_id)  # 更新LRU算法记录的未使用时间
                need_page_log, old_page_log, memory_page_log = True, old_page, dst_memory_page_id  # 记录可视化界面所需信息
        code_num_log, cur_code_log, code_page_log = self.code_num, current_code_id, code_page_id  # 记录可视化界面所需信息
        self.code_num += 1
        return code_num_log, cur_code_log, need_page_log, old_page_log, code_page_log, memory_page_log
