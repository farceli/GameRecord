import json
import prettytable  # 打印表格

'''
TODO:
    1、统计超过23:30游戏
    2、按月分组统计
    3、完善详细信息（P1）
'''

file_obj = open('har/17.har', 'r', encoding='utf-8')  # 打开文件
lines = file_obj.read()  # 读取全部内容
file_obj.close()  # 关闭文件
dict_str = json.loads(lines)  # 字符串转字典
entries = dict_str['log']['entries']  # 获取entries节点
table = prettytable.PrettyTable(['游戏开始时间', '游戏结果'])  # 创建表格Title
deduplication = []  # 初始化去重列表，用于存放每一个game_time

for entries_index in range(1, len(entries)):
    r = json.dumps(entries[entries_index]['response']['content']['text'])  # 获取text节点
    result = ''  # 初始化去除转义符号后的字符串

    # 去除转义符并删除首位双引号
    for i in r:
        if i != '\\':
            result += i
    result = result[1:-1]

    data_list = json.loads(result)['data']['list']  # 字符串转字典后获取list节点

    # 统计每局游戏详细信息
    for detailed in data_list:
        game_time = detailed['gametime']  # 获取游戏开始时间

        # 获取游戏结果
        game_result = ''
        if detailed['gameresult'] == 1:
            game_result = '胜利'
        elif detailed['gameresult'] == 2:
            game_result = '失败'
        else:
            ame_result = '特殊游戏结果'

        table.add_row([game_time, game_result])  # 将每一项添加到表格中
        deduplication.append(game_time)  # 把每一个gametile添加到去重列表中

print(table)  # 打印游戏详细信息表格

# 检查是否有重复日期
for a in range(len(deduplication)):
    for b in range(len(deduplication)):
        if a != b:
            if deduplication[a] == deduplication[b]:
                print("有重复")
                break

report = prettytable.PrettyTable(['时间段', '数量', '开游戏时间>23:30的数量'])  # 创建报告表格Title
report.add_row([min(deduplication) + ' ~ ' + max(deduplication), len(deduplication), 'nil'])  # 想报告表格中插入内容
print(report)  # 打印报告表格
