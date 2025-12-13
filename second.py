import streamlit as st
import pandas as pd
import numpy as np
# 定义数据,以便创建数据框
data = {
    '门店':['星怡会尝不忘','老友粉','高峰柠檬鸭','好友缘','西冷牛排店'],
    '评分':[4.5,4.2,4.8,4.7,4.5],
}
# 根据上面创建的data，创建数据框
df = pd.DataFrame(data)
# 定义数据框所用的新索引
index = pd.Series([1,2,3,4,5] ,name='序号')
# 将新索引应用到数据框上
df.index = index

st.header("门店数据")
# 使用write()方法展示数据框
st.write(df)

st.header("餐厅评分")

st.subheader("设置x参数")
# 通过x指定月份所在这一列为条形图的x轴
st.bar_chart(df, x='门店')

# 修改df，用月份列作为df的索引，替换原有的索引
df.set_index('门店', inplace=True)

st.subheader("设置y参数")
# 通过y参数筛选只显示评分的数据
st.bar_chart(df, y='评分')

st.subheader("设置width、height和use_container_width参数")
# 通过width、height和use_container_width指定条形图的宽度和高度
st.bar_chart(df, width=400, height=300, use_container_width=False)




st.header("不同类型餐厅的价格")
# 定义数据,以便创建数据框
data_price = {
    '门店':['星怡会尝不忘','老友粉','高峰柠檬鸭','好友缘','西冷牛排店'],
    '价格':[6,7,8,7,15],
}
# 根据上面创建的data_price，创建数据框
df = pd.DataFrame(data_price)
# 定义数据框所用的新索引
index = pd.Series([1,2,3,4,5], name='序号')
# 将新索引应用到数据框上
df.index = index

st.header("门店数据")
# 使用write()方法展示数据框
st.write(df)
st.header("折线图")

st.subheader("设置x参数")
# 通过x指定门店所在这一列为折线图的x轴
st.line_chart(df, x='门店')


# 修改df，用月份列作为df的索引，替换原有的索引
df.set_index('门店', inplace=True)

st.subheader("设置y参数")
# 通过y参数筛选只显示价格的数据
st.line_chart(df, y='价格')

st.subheader("设置width、height和use_container_width参数")
# 通过width、height和use_container_width指定折线图的宽度和高度
st.line_chart(df, width=300, height=300, use_container_width=False)



st.header("用餐高峰时段")
# 定义数据,以便创建数据框
data_time = {
     '时间':[9, 10, 11,12,13,14,15,16,17,18,19,20,21,22,23],
    '星怡会尝不忘':[200, 150, 180,300,200,100,120,80,200,400,300,200,100,120,50],
    '老友粉':[120, 160, 123,300,200,100,120,80,200,400,120,200,100,120,50],
    '高峰柠檬鸭':[110, 100, 160,300,200,100,120,80,200,300,300,200,100,120,50],
	'好友缘':[110, 100, 160,300,200,100,120,80,200,300,300,200,100,120,50],
	'西冷牛排店':[120, 160, 123,300,200,100,120,80,150,400,300,200,100,120,50]
}
# 根据上面创建的data，创建数据框
df = pd.DataFrame(data_time)
# 定义数据框所用的新索引
index = pd.Series([1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15], name='序号')
# 将新索引应用到数据框上
df.index = index

st.header("门店数据")
# 使用write()方法展示数据框
st.write(df)
st.header("面积图")

st.subheader("设置x参数")
# 通过x指定时间所在这一列为面积图的x轴
st.area_chart(df, x='时间')

# 修改df，用时间列作为df的索引，替换原有的索引
df.set_index('时间', inplace=True)

st.subheader("设置y参数")
# 通过y参数筛选只显示星怡会尝不忘的数据
st.area_chart(df, y='星怡会尝不忘')
# 通过y参数筛选只显示剩余门店的数据
st.area_chart(df, y=['老友粉','高峰柠檬鸭','好友缘','西冷牛排店'])

st.subheader("设置width、height和use_container_width参数")
# 通过width、height和use_container_width指定面积图的宽度和高度
st.area_chart(df, width=300, height=300, use_container_width=False)


st.header("餐厅位置")
# 定义数据,以便创建数据框
data_location = {
    '星怡会尝不忘':[22.853838, 108.222177],
    '老友粉':[22.863838, 108.232177],
    '高峰柠檬鸭':[22.873838, 108.252177],
	'好友缘':[22.893838, 108.272177],
	'西冷牛排店':[22.823838, 108.282177],
}
# 根据上面创建的data，创建数据框
df = pd.DataFrame(data_location)
# 定义数据框所用的新索引
index = pd.Series(['j', 'w',], name='位置')
# 将新索引应用到数据框上
df.index = index

st.header("门店数据")
# 使用write()方法展示数据框
st.write(df)
