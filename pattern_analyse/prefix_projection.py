# class Access:
#     # 进程的pid
#     pid: int
#     # 进程名 python model.py
#     cmd: str
#     # 访存的时间戳
#     timestampe: int
#     # 读写类型：rd/wr
#     op_type: str
#     # 访存地址，待挖掘和预测的数据
#     addr: int

from typing import List, Dict
from collections import defaultdict, Counter

class Access:
    def __init__(self, pid: int, cmd: str, timestamp: int, op_type: str, addr: int, app_type: str):
        self.pid = pid
        self.cmd = cmd
        self.timestamp = timestamp
        self.op_type = op_type
        self.addr = addr
        self.app_type = app_type

def prefix_span(prefix: List[int], data: List[List[int]], min_support: int):
    """使用前缀投影方法挖掘频繁序列模式"""
    patterns = []
    counter = Counter()

    # 在所有序列中计数每个元素作为潜在前缀的出现次数
    for sequence in data:
        found = set()
        for element in sequence:
            if element not in found:
                counter[element] += 1
                found.add(element)

    # 对于每个频繁的元素，递归地调用前缀投影
    for element, count in counter.items():
        if count >= min_support:
            new_prefix = prefix + [element]
            patterns.append(new_prefix)
            new_data = [seq[seq.index(element) + 1:] for seq in data if element in seq]
            patterns.extend(prefix_span(new_prefix, new_data, min_support))

    return patterns

def mine_sequences(data: List[Access], min_support: int) -> List[List[Access]]:
    """从Access对象列表中挖掘频繁访问模式"""
    # 将数据转换为按pid分组的地址序列
    grouped_data = defaultdict(list)
    access_map = defaultdict(list)
    for access in data:
        grouped_data[access.pid].append(access.addr)
        access_map[(access.pid, access.addr)].append(access)

    # 对每个pid的序列使用前缀投影挖掘频繁模式
    results = []
    for pid, sequences in grouped_data.items():
        # 调用前缀投影来挖掘频繁模式
        frequent_patterns = prefix_span([], [sequences], min_support)
        for pattern in frequent_patterns:
            # 对于每个模式，获取对应的Access对象列表
            pattern_accesses = [access_map[(pid, addr)][0] for addr in pattern]  # 取第一个匹配的Access对象
            results.append(pattern_accesses)

    return results

# 示例数据
data = [
    Access(pid=1, cmd="python model.py", timestamp=1622548672, op_type="rd", addr=123, app_type="ML"),
    Access(pid=1, cmd="python model.py", timestamp=1622548673, op_type="wr", addr=124, app_type="ML"),
    Access(pid=1, cmd="python model.py", timestamp=1622548674, op_type="rd", addr=123, app_type="ML"),
    Access(pid=2, cmd="python analyze.py", timestamp=1622548675, op_type="rd", addr=123, app_type="preprocess"),
    Access(pid=2, cmd="python analyze.py", timestamp=1622548676, op_type="rd", addr=125, app_type="preprocess"),
    Access(pid=2, cmd="python analyze.py", timestamp=1622548677, op_type="rd", addr=123, app_type="preprocess"),
    Access(pid=1, cmd="python model.py", timestamp=1622548675, op_type="rd", addr=125, app_type="ML"),
    Access(pid=1, cmd="python model.py", timestamp=1622548676, op_type="rd", addr=88, app_type="ML"),
    Access(pid=1, cmd="python model.py", timestamp=1622548674, op_type="rd", addr=126, app_type="ML"),
]

# 调用挖掘函数
predicted_accesses = mine_sequences(data, min_support=2)
for accesses in predicted_accesses:
    print("Pattern:")
    for access in accesses:
        print(f"PID: {access.pid}, Command: {access.cmd}, Timestamp: {access.timestamp}, Operation: {access.op_type}, Address: {access.addr}")
