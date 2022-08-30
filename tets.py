import configparser  # 读取ini

lists = {}
config = configparser.ConfigParser()
config.read("config/allconf.ini", encoding="utf-8")
# 修改ini 不存在会创建
# config.set('amount', 'game', '120')
# config.write(open('config/allconf.ini','w'))

for sections in config.sections():
    for options in config.options(sections):
        lists[sections + '_' + options] = config.get(sections, options)

print(lists)
