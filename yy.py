import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, time

# 页面基础配置（全局只需要设置一次，放在最顶部）
st.set_page_config(
    page_title="我所做过的内容",
    page_icon="📂",
    layout="wide"  # 宽布局适配侧边栏+内容
)

# ------------------- 左侧侧边导航栏（纵向） -------------------
st.sidebar.title("导航菜单")
# 侧边栏选择框（替代原来的tabs）
selected_menu = st.sidebar.selectbox(
    "选择内容",
    ["数字档案", "美食数据仪表", "相册", "音乐播放器", "视频网站", "个人简历生成器"]
)

# ------------------- 右侧内容区域（根据侧边栏选择展示对应内容） -------------------
# 1. 数字档案
if selected_menu == "数字档案":
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

    # 进度条
    st.subheader('Streamlit课程进度')
    st.text('Streamlit课程进度')
    st.progress(0.6)

    # 任务日志
    st.header("任务日志🚩")
    data = {
        '任务': ["学生数字档案", "课程管理系统", "数据图表展示"],
        '状态': ["完成😀", "进行中😅", "未完成😭"],
        '难度': ["🥰", "😟", "🙁"],
    }
    ind = pd.Series(['01月', '02月', '03月'], name='日期')
    df = pd.DataFrame(data, index=ind)
    st.dataframe(df)

    # 最新代码
    st.header("最新代码成果")
    st.caption("python代码")
    python_code = '''def hello():
    print("你好，Streamlit！")
    aaa
    ccc
    ccc
'''
    st.code(python_code, line_numbers=True)

    st.markdown(':green[>>>system message:] 下个任务已解锁')
    st.markdown(':green[>>>system message:] 下个任务已解锁')
    st.markdown(':green[>>>system message:] 下个任务已解锁')

# 2. 美食数据仪表（包含所有新增内容）
elif selected_menu == "美食数据仪表":
    st.header("门店数据（评分）")
    # 评分数据
    data = {
        '门店': ['星怡会尝不忘', '老友粉', '高峰柠檬鸭', '好友缘', '西冷牛排店'],
        '评分': [4.5, 4.2, 4.8, 4.7, 4.5],
    }
    df = pd.DataFrame(data)
    index = pd.Series([1, 2, 3, 4, 5], name='序号')
    df.index = index
    st.write(df)

    st.header("餐厅评分 - 条形图")
    st.subheader("设置x参数")
    st.bar_chart(df, x='门店')

    df.set_index('门店', inplace=True)
    st.subheader("设置y参数")
    st.bar_chart(df, y='评分')

    st.subheader("设置width、height和use_container_width参数")
    st.bar_chart(df, width=400, height=300, use_container_width=False)

    # 新增：不同类型餐厅的价格
    st.header("不同类型餐厅的价格")
    data_price = {
        '门店': ['星怡会尝不忘', '老友粉', '高峰柠檬鸭', '好友缘', '西冷牛排店'],
        '价格': [6, 7, 8, 7, 15],
    }
    df = pd.DataFrame(data_price)
    index = pd.Series([1, 2, 3, 4, 5], name='序号')
    df.index = index
    st.header("门店数据（价格）")
    st.write(df)

    st.header("餐厅价格 - 折线图")
    st.subheader("设置x参数")
    st.line_chart(df, x='门店')

    df.set_index('门店', inplace=True)
    st.subheader("设置y参数")
    st.line_chart(df, y='价格')

    st.subheader("设置width、height和use_container_width参数")
    st.line_chart(df, width=300, height=300, use_container_width=False)

    # 新增：用餐高峰时段
    st.header("用餐高峰时段")
    data_time = {
        '时间': [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
        '星怡会尝不忘': [200, 150, 180, 300, 200, 100, 120, 80, 200, 400, 300, 200, 100, 120, 50],
        '老友粉': [120, 160, 123, 300, 200, 100, 120, 80, 200, 400, 120, 200, 100, 120, 50],
        '高峰柠檬鸭': [110, 100, 160, 300, 200, 100, 120, 80, 200, 300, 300, 200, 100, 120, 50],
        '好友缘': [110, 100, 160, 300, 200, 100, 120, 80, 200, 300, 300, 200, 100, 120, 50],
        '西冷牛排店': [120, 160, 123, 300, 200, 100, 120, 80, 150, 400, 300, 200, 100, 120, 50]
    }
    df = pd.DataFrame(data_time)
    index = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], name='序号')
    df.index = index
    st.header("门店数据（高峰时段）")
    st.write(df)

    st.header("用餐高峰 - 面积图")
    st.subheader("设置x参数")
    st.area_chart(df, x='时间')

    df.set_index('时间', inplace=True)
    st.subheader("设置y参数")
    st.area_chart(df, y='星怡会尝不忘')
    st.area_chart(df, y=['老友粉', '高峰柠檬鸭', '好友缘', '西冷牛排店'])

    st.subheader("设置width、height和use_container_width参数")
    st.area_chart(df, width=300, height=300, use_container_width=False)

    # 新增：餐厅位置
    st.header("餐厅位置")
    data_location = {
        '星怡会尝不忘': [22.853838, 108.222177],
        '老友粉': [22.863838, 108.232177],
        '高峰柠檬鸭': [22.873838, 108.252177],
        '好友缘': [22.893838, 108.272177],
        '西冷牛排店': [22.823838, 108.282177],
    }
    df = pd.DataFrame(data_location)
    index = pd.Series(['纬度', '经度'], name='位置')  # 修正索引命名，更合理
    df.index = index
    st.header("门店数据（位置）")
    st.write(df)

    map_data = {
        "latitude": [22.853838, 22.965046, 22.812200, 22.809105, 22.839699],
        "longitude": [108.222177, 108.353921, 108.266629, 108.378664, 108.245804]
    }
    mp_df = pd.DataFrame(map_data)
    st.map(mp_df)

# 3. 相册
elif selected_menu == "相册":
    st.title("我的相册")
    # 初始化图片索引（独立命名，避免冲突）
    if 'img_ind' not in st.session_state:
        st.session_state['img_ind'] = 0

    images = [
        {
            'url': "https://www.baltana.com/files/wallpapers-2/Cute-Cat-Images-07756.jpg",
            'text': '猫'
        },
        {
            'url': "https://cdn.britannica.com/82/232782-050-8062ACFA/Black-labrador-retriever-dog.jpg",
            'text': '狗'
        },
        {
            'url': "https://live.staticflickr.com/2686/4497672316_d283310530_3k.jpg",
            'text': '狮子'
        }
    ]

    # 展示当前图片
    st.image(images[st.session_state['img_ind']]['url'], caption=images[st.session_state['img_ind']]['text'])

    # 切换图片函数（区分上一张/下一张）
    def change_img(direction):
        if direction == "next":
            st.session_state['img_ind'] = (st.session_state['img_ind'] + 1) % len(images)
        else:
            st.session_state['img_ind'] = (st.session_state['img_ind'] - 1) % len(images)

    # 切换按钮
    c1, c2 = st.columns(2)
    with c1:
        st.button("上一张", on_click=change_img, args=["prev"], use_container_width=True)
    with c2:
        st.button("下一张", on_click=change_img, args=["next"], use_container_width=True)

# 4. 音乐播放器
elif selected_menu == "音乐播放器":
    st.title("我的音乐播放器🎵")
    # 初始化音乐索引（独立命名）
    if 'music_ind' not in st.session_state:
        st.session_state['music_ind'] = 0

    musics = [
        {
            'audio_url': 'https://music.163.com/song/media/outer/url?id=251400938.mp3',
            'poster_url': 'http://p2.music.126.net/UiXCbh42gRUxRyZL_hllKQ==/109951170062464612.jpg?param=177y177',
            'title': '匿名的好友',
            'singer': 'en',
            'duration': '3:55'
        },
        {
            'audio_url': 'https://music.163.com/song/media/outer/url?id=2668397359.mp3',
            'poster_url': 'http://p1.music.126.net/-NVLOT5vt9I91LRiZV1TCQ==/109951170413587092.jpg?param=130y130',
            'title': '晴天',
            'singer': '周杰伦',
            'duration': '4:29'
        },
        {
            'audio_url': 'https://music.163.com/song/media/outer/url?id=2146737748.mp3',
            'poster_url': 'http://p2.music.126.net/YOXrZt0Nw5CPzH03KhUXdQ==/109951169504798220.jpg?param=130y130',
            'title': '稻香',
            'singer': '周杰伦',
            'duration': '3:43'
        }
    ]

    # 切换音乐函数
    def prev_music():
        st.session_state['music_ind'] = (st.session_state['music_ind'] - 1) % len(musics)

    def next_music():
        st.session_state['music_ind'] = (st.session_state['music_ind'] + 1) % len(musics)

    # 布局：封面+信息+播放器
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(
            musics[st.session_state['music_ind']]['poster_url'],
            caption="专辑封面",
            width="stretch"
        )
    with col2:
        st.subheader(f"《{musics[st.session_state['music_ind']]['title']}》")
        st.caption(f"歌手：{musics[st.session_state['music_ind']]['singer']} | 时长：{musics[st.session_state['music_ind']]['duration']}")
        st.audio(
            data=musics[st.session_state['music_ind']]['audio_url'],
            format="audio/mp3",
            autoplay=False
        )

    # 控制按钮
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.button("⏮️上一曲", on_click=prev_music, use_container_width=True)
    with btn_col2:
        st.button("下一曲⏭️", on_click=next_music, use_container_width=True)

# 5. 视频网站
elif selected_menu == "视频网站":
    st.title("红楼梦第一部📺")
    # 视频列表
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

    # 剧情介绍
    episode_intro = [
        "空空道人路经大荒山，惊见孤石凿刻前世今生：“无才补天，幻形入世，蒙茫茫大士，渺渺真人携入红尘，历尽离合悲欢炎凉世态的传奇”。据石偈坠落之乡，追述至姑苏城里乡宦甄士隐之身世，演绎一生荣枯。更有甄士隐受神灵旨意，梦中和幻化巨石为玉的僧道相遇，验证天地之精华，投胎前生之真身，好不一般。但甄士隐虽神仙一流人品，只一事不足，年已半百，膝下只有一女，却神奇般遗失，运道败落，随了僧道西去。",
        "黛玉进了贾府，处处小心在意。宝黛初会，二人都认为对方是前世见过的，格外亲密。贾雨村和贾府连了宗，立刻走马上任。门子献给贾雨村一张护官符，上面列明贾史王薛四大家族。其中薛家的薛蟠打死人命，贾雨村却听了门子的话给胡乱了结了。薛蟠高高兴兴带着薛姨妈和薛宝钗上京，暂住在贾府。宁国府家宴，宝玉喝醉后睡在秦可卿房中，梦游太虚幻境，见到一位神仙姐姐。",
        "因无法融入宁府的气氛，宝玉到秦可卿房中午睡。梦中来到太虚幻境，既读到了家族女儿悲欢，又被“可卿”教授了云雨之欢，醒后与袭人共试。而同时黛玉也已不再生气，小风波平息。谈及“穷人攀富”，引出刘姥姥进荣国府攀亲求财。凤姐趾高气扬地在刘姥姥面前做足贵族架子，恩赐了不在乎的一点银子，却是刘姥姥的救命钱。",
        "薛姨妈处有精美的宫花，周瑞家的将宫花送给各人，只有黛玉不愿接受。宁府的尤氏请凤姐过去玩乐，宝玉随去，无意中遇见了秦可卿的弟弟秦钟，宝玉十分喜欢，邀他到贾府念书。宝玉想起宝钗小病，前去探望，两人拿出宝玉和金璎珞，互相比看，不料黛玉来了，打趣他们。宝玉喝醉回房，趁酒意大骂李嬷嬷。秦家恭敬的领了秦钟来贾府，等着一起读书。",
        "宝玉和秦钟一起上学，但是无心读书，只是眉来眼去，勾留美貌的小学生。一日，薛蟠不在，薛蟠的旧好和秦钟有意，被同学金荣所奚落，茗烟冲进学堂大骂，金荣等和宝玉的小厮们大打出手，大闹学堂。金荣的亲戚金氏来尤氏面前告状，却得知秦可卿重病缠身，不禁噤声离去。尤氏不知秦可卿究竟何病，十分好奇，贾珍派人请来张先生给秦可卿诊病。看似医术高明，贾珍等仍旧忧心。"
    ]

    # 初始化视频索引（独立命名）
    if 'video_ind' not in st.session_state:
        st.session_state['video_ind'] = 0

    # 显示当前集数信息
    current_ind = st.session_state['video_ind']
    st.text(f"【{video_arr[current_ind]['title']}剧情介绍】")
    st.text(episode_intro[current_ind])
    st.video(video_arr[current_ind]['url'], autoplay=True)

    # 切换集数函数
    def play_episode(i):
        st.session_state['video_ind'] = int(i)

    # 集数按钮
    cols = st.columns(3)
    for idx, i in enumerate(range(len(video_arr))):
        col_idx = idx % 3
        with cols[col_idx]:
            st.button(
                f'第{i + 1}集',
                use_container_width=True,
                on_click=play_episode,
                args=[i]
            )

    # 红楼梦介绍
    st.header('关于《红楼梦》📖')
    st.caption('红楼梦简介')
    st.text('《红楼梦》，中国古代章回体长篇小说，中国古典四大名著之一。其通行本共120回，一般认为前80回是清代作家曹雪芹所著，后40回作者为无名氏，整理者为程伟元、高鹗。')
    st.text('《红楼梦》以贾、史、王、薛四大家族的兴衰为背景，以富贵公子贾宝玉为视角，以贾宝玉与林黛玉、薛宝钗的爱情婚姻悲剧为主线，描绘了一些闺阁佳人的人生百态，展现了真正的人性美和悲剧美，是一部从各个角度展现女性美以及中国古代社会百态的史诗性著作。')
    st.text('《红楼梦》版本有120回“程本”和80回“脂本”两大系统。程本为程伟元排印的印刷本，脂本为脂砚斋在不同时期抄评的早期手抄本。脂本是程本的底本。')
    st.text('《红楼梦》是一部具有世界影响力的人情小说、中国封建社会的百科全书、传统文化的集大成者。其作者以“大旨谈情，实录其事”自勉，只按自己的事体情理，按迹循踪，摆脱旧套，新鲜别致，取得了非凡的艺术成就。“真事隐去，假语存焉”的特殊笔法更是令后世读者脑洞大开，揣测之说久而遂多。二十世纪以来，《红楼梦》更以其丰富深刻的思想底蕴和异常出色的艺术成就使学术界产生了以其为研究对象的专门学问——红学。')

# 6. 个人简历生成器
elif selected_menu == "个人简历生成器":
    st.header("个人简历生成器")
    # 分栏：左表单、右预览
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        with st.form("info_form", clear_on_submit=False):
            st.subheader("个人信息表单")
            name = st.text_input("姓名")
            gender = st.selectbox("性别", ["男", "女", "其他"])
            phone = st.text_input("电话")
            email = st.text_input("邮箱")
            birth_date = st.date_input("出生日期", value=date(1990, 1, 1))
            edu_bg = st.selectbox("学历", ["本科", "专科", "硕士", "博士"])
            position = st.selectbox("职位", ["软件工程", "前端开发", "后端开发", "产品经理", "其他"])
            work_exp = st.selectbox("工作经验", ["0年", "1-3年", "3-5年", "5年以上"])
            salary_min = st.slider("期望薪资(下限)", 10000, 50000, 10000)
            salary_max = st.slider("期望薪资(上限)", 10000, 50000, 20000)
            best_time = st.selectbox("最佳联系时间", ["09:00", "10:00", "14:00", "15:00"])
            lang_skill = st.selectbox("语言能力", ["英语", "法语", "俄语", "德语", "其他"])
            intro = st.text_area("个人简介", "这个人很神秘，没有留下任何介绍。")
            photo = st.file_uploader("选择照片", type=["jpg", "png", "jpeg"])
            submit_btn = st.form_submit_button("更新简历")

    with col2:
        st.subheader("简历实时预览")
        if submit_btn and photo:
            st.image(photo, width=200, caption="本人照片")

        # 信息分栏
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.write(f"姓名:{name}")
            st.write(f"职位: {position}")
            st.write(f"电话: {phone if phone else ''}")
            st.write(f"邮箱: {email if email else ''}")
            st.write(f"出生日期: {birth_date}")
        with info_col2:
            st.write(f"性别: {gender}")
            st.write(f"学历: {edu_bg}")
            st.write(f"工作经验: {work_exp}")
            st.write(f"期望薪资: {salary_min}-{salary_max}元")
            st.write(f"最佳联系时间: {best_time}")
            st.write(f"语言能力: {lang_skill}")

        # 个人简介
        st.markdown("---")
        st.subheader("个人简介")
        st.write(intro)
        st.caption('"代码改变世界，我改变代码"')
