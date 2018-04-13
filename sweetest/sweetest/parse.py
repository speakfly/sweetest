from sweetest.log import logger
from sweetest.config import all_keywords, comma_lower, comma_upper, equals, vertical
from sweetest.elements import e
from sweetest.globals import g


def escape(data):
    # 先把转义字符替换掉
    return data.replace('\\,', comma_lower).replace('\\，', comma_upper).replace('\\=', equals)


def recover(data):
    # 再把转义字符恢复
    return data.replace(comma_lower, ',').replace(comma_upper, '，').replace(equals, '=')


def elements_format(page, element):

    if not element:
        return page, '', element

    if page in ('SNIPPET','用例片段') or element in ('变量赋值',):
        return page, '', element

    frame, el = e.have(page, element)
    return page, frame, el


def check_keyword(action):
    try:
        keyword = all_keywords.get(action)
        return keyword
    except:
        logger.exception('Keyword:%s is not exist' % action)
        exit()


def data_format(data):
    data = escape(data)
    data = data.replace('，', ',')
    data_list = {}
    if data:
        data_list = data.split(',')
    data_dict = {}
    for data in data_list:
        # 只需要分割第一个'='号
        d = data.split('=', 1)
        d[-1] = recover(d[-1])  # 只有值需要转义恢复，<元素属性> or <变量名> 不应该出现转义字符
        if len(d) == 1:
            # 如果没有=号分割，说明只有内容，默认赋值给 text
            data_dict['text'] = d[0]
        elif len(d) == 2:
            d[0] = d[0].strip()  # 清除 <元素属性> 2边的空格，如果有的话
            data_dict[d[0]] = d[1]
        else:
            raise Exception('Error: Testcase\'s Data is error, more "=" or less ","')
    return data_dict


def parse(testsuit):
    '''
    将测试用例解析为可执行参数，如:
    打开首页，解析为：OPEN 127.0.0.1
    '''
    for testcase in testsuit:
        for step in testcase['steps']:
            step['keyword'] = check_keyword(step['keyword'])
            step['page'], step['frame'], step['element'] = elements_format(step['page'], step['element'])
            step['data'] = data_format(str(step['data']))
            step['output'] = data_format(step['output'])
