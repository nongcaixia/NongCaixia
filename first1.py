import streamlit as st

st.set_page_config(page_title="电影世界", page_icon="🎬")
st.title("红楼梦第一部")

video_arr = [
    {
        'url': 'https://www.w3school.com.cn/example/html5/mov_bbb.mp4',
        'title': '第1集'
    },
    {
        'url': 'https://www.w3schools.com/html/movie.mp4',
        'title': '第2集'
    },
    {
        'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'title': '第3集'
    },
    {
        'url': 'https://www.w3schools.com/html/movie.mp4',
        'title': '第4集'
    },
    {
        'url': 'https://media.w3.org/2010/05/sintel/trailer.mp4',
        'title': '第5集'
    }
]

# 检查session_state中有没有ind
if 'ind' not in st.session_state:
    st.session_state['ind'] = 0

# 显示视频
st.video(video_arr[st.session_state['ind']]['url'], autoplay=True)

# 切换集数的函数
def play(i):
    st.session_state['ind'] = int(i)

# 核心修改：创建三列布局，循环将按钮放入对应列
cols = st.columns(3)  # 创建3个等宽列
for idx, i in enumerate(range(len(video_arr))):
    # 按索引取模3，决定放入哪一列（0=第一列，1=第二列，2=第三列）
    col_idx = idx % 3
    with cols[col_idx]:
        st.button(
            f'第{i + 1}集',
            use_container_width=True,
            on_click=play,
            args=[i]  # 注意：args是列表，不需要双层括号（原代码的[i]改成i即可）
        )