"""采集商品评论数据"""
import requests
import pandas as pd


lis = []
for page in range(1, 21):

    url = 'https://club.jd.com/comment/productPageComments.action'
    data = {
        # 'callback': 'fetchJSON_comment98',
        'productId': '100024427082',
        'score': '0',
        'sortType': '5',
        'page': page,
        'pageSize': '10',
        'isShadowSku': '0',
        'rid': '0',
        'fold': '1',
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url,params=data,headers=headers)
    # simplejson.errors.JSONDecodeError: Expecting value: line 1 column 1 (char 0)   不是完整的jison数据
    comments =response.json()['comments']
    lis = []
    for index in comments:
        content = index['content']  # 评论内容
        date = index['creationTime']  # 评论时间
        product = index['productColor']  # 购买商品
        name = index['nickname']  # 用户昵称
        kind = index['referenceName']  # 购买套餐
        score = index['score']  # 用户评分
        dic = {
            '评论内容': content,
            '评论时间': date,
            '购买商品': product,
            '用户昵称': name,
            '购买套餐': kind,
            '用户评分': score
        }
        print(dic)
        lis.append(dic)
        with open('口红.txt', mode='a', encoding='utf-8') as f:
            f.write(content)
            f.write('\n')


# 爬取的评论信息保存为xlsx格式
# pd_data = pd.DataFrame(lis)
# pd_data.to_excel('口红2.xlsx', index=False)
