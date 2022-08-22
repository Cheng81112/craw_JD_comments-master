import wordcloud
import jieba


f = open(f'口红.txt', encoding='utf-8')  # 打开文件
text = f.read()
print(text)

txt_list = jieba.lcut(text)   # 分割词汇
print(txt_list)
string = ' '.join(txt_list)

wc = wordcloud.WordCloud(
    width=500,
    height=500,
    background_color='white',  # 背景颜色
    font_path='msyh.ttc',  # 字体文件
)

wc.generate(string)
wc.to_file(f'商品评论词云图.png')
