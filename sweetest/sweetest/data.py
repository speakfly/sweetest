import xlrd
from sweetest.utility import Excel, data2dict
from sweetest.config import header


def testsuite_format(data):
    '''
    将元素为 dict 的 list，处理为 testcase 的 list
    testcase 的格式：
    {
        'id': 'Login_001',  #用例编号
        'title': 'Login OK',  #用例标题
        'condition': '',  #前置条件
        'designer': 'Leo',  #设计者
        'flag': '',  #自动化标记
        'result': '',  #测试结果
        'remark': '',  #备注
        'steps':
            [
                {
                'no': 1,  #步骤编号
                'action': '输入',
                'page': '产品管系统登录页',
                'elements': '用户名'
                'data': 'user1',  #测试数据
                'output': '',  #输出数据
                'result': '',  #测试结果
                'remark': ''  #备注
                },
                {……}
                ……
            ]
    }
    '''
    testsuite = []
    testcase = {}
    data = data2dict(data)

    for d in data:
        # 如果用例编号不为空，则为新的用例
        if d['id'].strip():
            # 如果 testcase 非空，则添加到 testcases 里，并重新初始化 testcase
            if testcase:
                testsuite.append(testcase)
                testcase = {}
            for key in ('id', 'title', 'condition', 'designer', 'flag', 'result', 'remark'):
                testcase[key] = d[key]
            testcase['priority'] = d.get('priority', 'M')
            testcase['steps'] = []
        # 如果步骤编号不为空，则为有效步骤，否则用例解析结束
        no = str(d['step']).strip()
        if no:
            step = {}
            step['control'] = ''
            if no[0] in ('^', '>', '<', '#'):
                step['control'] = no[0]
                step['no'] = no
            else:
                step['no'] = int(d['step'])
            for key in ('keyword', 'page', 'element', 'data', 'output', 'score', 'remark'):
                step[key] = d[key]

            # 仅作为测试结果输出时，保持原样
            step['_keyword'] = d['keyword']
            step['_element'] = d['element']
            step['_data'] = d['data']
            step['_output'] = d['output']
            testcase['steps'].append(step)
    if testcase:
        testsuite.append(testcase)
    return testsuite


def testsuite_from_excel(file_name, sheet_name):
    d = Excel(file_name)
    return testsuite_format(data2dict(d.read(sheet_name)))


def testsuite2data(data):
    result = [list(header.keys())]
    for d in data:
        s = d['steps'][0]  # 第一步和用例标题同一行
        testcase = [d['id'], d['title'], d['condition'], s['no'], s['_keyword'], s['page'], s['_element'],
                s['_data'], s['_output'], d['priority'], d['designer'], d['flag'], s['score'], d['result'], s['remark']]
        result.append(testcase)
        for s in d['steps'][1:]:
            step = ['', '', '', s['no'], s['_keyword'], s['page'], s['_element'],
                    s['_data'], s['_output'], '', '', '', s['score'], '', s['remark']]
            result.append(step)
    return result
