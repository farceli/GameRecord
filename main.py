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
    ini_dict['harPath_wx'] = dict(con.items('har_path'))['wx']
    ini_dict['harPath_qq'] = dict(con.items('har_path'))['qq']
    return ini_dict


# 初始化
# bark_url = read_config()['barkUrl_farceLi']  # 初始化bark_url(FarceLi)
bark_url = read_config()['qiaoqiao']  # 初始化bark_url(qiaoqiao)
harPath_wx = read_config()['harPath_wx']  # 初始化harPath_wx
harPath_qq = read_config()['harPath_qq']  # 初始化harPath_qq


def test(file_obj, area):
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
            statistical_period = '\n统计周期：' + start_time + '-30 00:00 ~ ' + max(month_game_list)
            number_of_games = '\n游戏数量：' + str(len(month_game_list)) + '（上限：120）'
            bark_body = current_cycle_body + statistical_period + number_of_games
            bark_url = bark_url + bark_title + bark_body
            requests.get(url=bark_url)

    print(report)  # 打印报告表格


file_obj = open(harPath_wx, 'r', encoding='utf-8')  # 打开文件wx
test(file_obj, 'wx')
file_obj = open(harPath_qq, 'r', encoding='utf-8')  # 打开文件qq
test(file_obj, 'qq')
