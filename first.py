import streamlit as st
import pandas as pd
st.title('--学生 小陆👧-数字档案')
st.header('📝基础信息')
st.markdown('学生ID: NEO-2023-001')
st.markdown('注册时间: :green[2023-10-01 08:30:17]|精神状态:正常')
st.markdown('当前教室: :green[实训楼301]|安全等级: :green[绝密]')
st.header('🛠️技能矩阵')
c1, c2, c3 = st.columns(3)
c1.metric(label="C语言", value="95℃", delta="2%")
c2.metric(label="python", value="87%", delta="-1%")
c3.metric(label="java", value="68%", delta="-10%")
#制作进度条
st.subheader('Streamlit课程进度')
st.text('Streamlit课程进度')
st.progress(0.6)

# 定义列布局，分成3列
st.header("任务日志🚩")
#写数据，制作成表
data = {
    '任务':["学生数字档案", "课程管理系统", "数据图表展示"],
    '状态':["完成😀", "进行中😅","未完成😭"],
    '难度':["🥰","😟", "🙁"],
}
ind = pd.Series(['01月', '02月', '03月'], name='日期')
df = pd.DataFrame(data, index=ind)
st.dataframe(df)
st.header("最新代码成果")
st.caption("python代码")
python_code = '''def hello():
    print("你好，Streamlit！")
    aaa
    ccc
    ccc
'''
#展示代码和列数
st.code(python_code, line_numbers=True)

st.markdown(':green[>>>system message:] 下个任务已解锁') 
st.markdown(':green[>>>system message:] 下个任务已解锁') 
st.markdown(':green[>>>system message:] 下个任务已解锁') 