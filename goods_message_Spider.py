"""
主要工作：
selenium工具的使用  稳定
结构化的数据解析
csv的数据保存
"""


'''
爬虫思路流程：
1、明确需求（不需要专门去做数据来源分析）
2、发送请求
3、获取数据
4、解析数据
5、保存数据
'''


import pymysql

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options



# 7.创建文件
key_word = input("请输入商品文件名：")
f = open(f'{key_word}商品信息采集表.csv', mode='a', encoding='utf-8', newline='')
csv_write = csv.DictWriter(f, fieldnames=[
    '标题',
    '价格',
    '评论量',
    '店铺名称',
    '详情页',
])
csv_write.writeheader() # 写入表头

# 无头浏览器设置
# 准备好参数配置
# opt = Options()
# opt.add_argument("--headless")
# opt.add_argument("--disbale-gpu")
#
# driver = Chrome(options=opt)  # 创建浏览器对象，把参数配置设置到浏览器中

# 1.实例化一个浏览器对象
driver = webdriver.Chrome()
# 2.请求网址
driver.get('https://www.jd.com/')
# 3.输入关键词
driver.find_element(By.XPATH, r'//*[@id="key"]').send_keys(key_word)
# 4.点击搜索按钮
driver.find_element(By.XPATH, r'//*[@id="search"]/div/div[2]/button/i').click()

# 5.下滑页面
def drop_down():
    """执行页面滚动的操作""" # javascript
    for x in range(1,12,3): # 1 3 5 7 9 在你不断的下滑过程中，页面高度也会变得
        time.sleep(1)
        j = x/9 # 1/9 3/9 5/9 9/9
        # document.documentElement.scrollTop 指定滑动条位置
        # document.documentElement.scrollHeight 获取浏览器页面最大高度
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % j
        driver.execute_script(js)

def get_shop_info():
    driver.implicitly_wait(10)  # 隐藏式等待，什么时候加载完数据 什么时候运行下面的步骤
    drop_down()
    # 6.获取所有商品li标签
    lis = driver.find_elements(By.CSS_SELECTOR, '#J_goodsList > ul > li')
    for li in lis:
        title = li.find_element(By.CSS_SELECTOR, '.p-name a em').text
        price = li.find_element(By.CSS_SELECTOR, '.p-price i').text
        comment_amount = li.find_element(By.CSS_SELECTOR, '.p-commit a').text
        shop_name = li.find_element(By.CSS_SELECTOR, '.p-shop a').text
        href = li.find_element(By.CSS_SELECTOR, '.p-name a').get_attribute('href')

        dic = {
            '标题': title,
            '价格': price,
            '评论量': comment_amount,
            '店铺名称': shop_name,
            '详情页': href
        }
        # 8.写入数据
        csv_write.writerow(dic)
        print(title, price, comment_amount, shop_name, href)

    # 模拟点击下一页
    driver.find_element(By.CSS_SELECTOR, '.pn-next').click()

# 爬取前4页的内容
for page in range(17,20):
    time.sleep(1) # 延时等待
    print(f"=============正在采集第{page}的数据内容=================")
    get_shop_info()
# 爬取一页的内容
get_shop_info()



driver.quit() # 采集完数自动关闭浏览器

print("商品信息采集结束")






