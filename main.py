import json
import time

import prettytable  # 打印表格
import requests
import tool.universalTool as Tool  # 自动以工具
import configparser  # 读取ini

'''
TODO:
    1、完善详细信息（P1）
'''


#  读取配置文件
def read_config():
    ini_dict = {}
    file = 'config/allconf.ini'
    con = configparser.ConfigParser()
    con.read(file, encoding='utf-8')
    ini_dict['barkUrl_farceLi'] = dict(con.items('bark_url'))['farceli']
    ini_dict['barkUrl_qiaoqiao'] = dict(con.items('bark_url'))['qiaoqiao']
    ini_dict['harPath_wx'] = dict(con.items('har_path'))['wx']
    ini_dict['harPath_qq'] = dict(con.items('har_path'))['qq']
    ini_dict['amount_game'] = dict(con.items('amount'))['game']
    return ini_dict


# 初始化
bark_url = read_config()['barkUrl_farceLi']  # 初始化bark_url(FarceLi)
# bark_url = read_config()['barkUrl_qiaoqiao']  # 初始化bark_url(qiaoqiao)
harPath_wx = read_config()['harPath_wx']  # 初始化harPath_wx
harPath_qq = read_config()['harPath_qq']  # 初始化harPath_qq

update_data = {
    'amount_game': [{
        'time': '2022-08-20',
        'reason': '李奥琦拖鞋忘记放在鞋架上',
        'type': 'add',
        'num': 10
    }, {
        'time': '2022-08-26',
        'reason': '李奥琦扣头',
        'type': 'add',
        'num': 10
    }, {
        'time': '2022-08-27',
        'reason': '李奥琦拖鞋忘记放在鞋架上',
        'type': 'add',
        'num': 10
    }],
    'other game': [
        '08-21 17:35',
        '08-21 17:18'
    ]
}


def test(file_obj, area):
    amount_game = int(read_config()['amount_game'])  # 初始化游戏局数

    lines = file_obj.read()  # 读取全部内容
    file_obj.close()  # 关闭文件
    dict_str = json.loads(lines)  # 字符串转字典
    entries = dict_str['log']['entries']  # 获取entries节点
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
            deduplication.append(game_time)  # 把每一个gametile添加到去重列表中
            # # 获取游戏结果
            # game_result = ''
            # if detailed['gameresult'] == 1:
            #     game_result = '胜利'
            # elif detailed['gameresult'] == 2:
            #     game_result = '失败'
            # else:
            #     ame_result = '特殊游戏结果'
            #
            # if game_time[-5:] >= '23:30':
            #     table.add_row(['\033[31m' + game_time + '\033[0m', game_result])  # 将每一项添加到表格中
            # else:
            #     table.add_row([game_time, game_result])

    # 检查是否有重复日期
    for a in range(len(deduplication)):
        for b in range(len(deduplication)):
            if a != b:
                if deduplication[a] == deduplication[b]:
                    print("有重复")
                    break

    if len(update_data) != 0:
        if len(update_data['amount_game']) != 0:
            for i in range(len(update_data['amount_game'])):
                if update_data['amount_game'][i]['type'] == 'add':
                    amount_game += update_data['amount_game'][i]['num']
                elif update_data['amount_game'][i]['type'] == 'reduce':
                    amount_game -= update_data['amount_game'][i]['num']
                else:
                    print(Tool.red_text('Err'))
        if len(update_data['other game']) != 0:
            for i in range(len(update_data['other game'])):
                if update_data['other game'][i] in deduplication:
                    # print(update_data['other game'][i])
                    deduplication.remove(update_data['other game'][i])
                # print(type(update_data['other game'][i]))
                # print(type(deduplication[0]))

    report = prettytable.PrettyTable(['时间段', '详细对局', '数量', '开游戏时间>23:30的数量'])  # 创建报告表格Title
    report.add_row(
        [min(deduplication) + ' ~ ' + max(deduplication), 'All in', len(deduplication), 'nil'])  # 想报告表格中插入内容

    # 把列表变成n个一组的字符串
    def for_list(list_param):
        list_len = 1
        list_str = ''
        for i in list_param:
            if list_len % 10 == 0 or list_len == len(list_param):
                list_str += i + '\n'
            else:
                list_str += i + '    '
            list_len += 1
        return list_str

    for month in range(1, 13):
        start_time = ''
        end_time = ''
        month_game_list = []
        number_of_timeouts = 0  # 初始化超过23:30分游戏的数量
        if month == 9:
            start_time = '0' + str(month)
            end_time = str(month + 1)
        elif len(str(month)) == 1 and month != 9:
            start_time = '0' + str(month)
            end_time = '0' + str(month + 1)
        elif month == 12:
            start_time = str(month)
            end_time = '01'
        else:
            start_time = str(month)
            end_time = str(month + 1)

        title = start_time + '-30 00:00 ~ ' + end_time + '-29 23:59'
        for i in deduplication:
            if start_time + '-30 00:00' <= i <= end_time + '-29 23:59':
                if i[-5:] >= '23:30':
                    month_game_list.append(Tool.red_text(i))
                    number_of_timeouts += 1
                else:
                    month_game_list.append(i)
        if number_of_timeouts != 0:
            report.add_row(
                [title, for_list(month_game_list), len(month_game_list), Tool.red_text(str(number_of_timeouts))])
        else:
            report.add_row([title, for_list(month_game_list), len(month_game_list), number_of_timeouts])

        current_time = time.strftime('%m-%d %H:%M')
        if start_time + '-30 00:00 ~ ' <= current_time <= end_time + '-29 23:59':
            if area == 'wx':
                bark_title = '[微信区]王者荣耀当前周期战绩推送/'
            elif area == 'qq':
                bark_title = '[QQ区]王者荣耀当前周期战绩推送/'
            else:
                print("Err")

            current_cycle_body = '当前周期：' + title  # 当前周期
            statistical_period_body = '\n统计周期：' + start_time + '-30 00:00 ~ ' + max(month_game_list)
            number_of_games_body = '\n游戏数量：' + str(len(month_game_list)) + '（上限：' + str(amount_game) + '）'
            number_of_timeouts_body = '\n超时数量：' + str(number_of_timeouts)
            bark_body = current_cycle_body + statistical_period_body + number_of_games_body + number_of_timeouts_body
            requests_bark_url = bark_url + bark_title + bark_body
            requests.get(url=requests_bark_url)

    print(report)  # 打印报告表格


file_obj = open(harPath_wx, 'r', encoding='utf-8')  # 打开文件wx
test(file_obj, 'wx')
file_obj = open(harPath_qq, 'r', encoding='utf-8')  # 打开文件qq
test(file_obj, 'qq')
