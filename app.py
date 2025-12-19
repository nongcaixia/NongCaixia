import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go  
import joblib
import numpy as np
from scipy import stats  

# ---------------------- 全局配置 ----------------------
st.set_page_config(page_title="学生成绩分析与预测系统", page_icon="📊", layout="wide")

# 加载数据、模型和专业列表
@st.cache_data  
def load_data():
    df = pd.read_csv("student_data_adjusted_rounded.csv")
    df.columns = ["学号", "性别", "专业", "每周学习时长（小时）", "上课出勤率", "期中考试分数", "作业完成率", "期末考试分数"]
    df = df.dropna()  
    return df

model = joblib.load("score_prediction_model.pkl")
majors = joblib.load("majors_list.pkl")
df = load_data()

# ---------------------- 侧边栏导航 ----------------------
st.sidebar.title("导航菜单")
page = st.sidebar.radio(
    "选择功能界面",
    ["项目介绍", "专业成绩分析", "期末成绩预测"]
)

# ---------------------- 界面1：项目介绍 ----------------------
if page == "项目介绍":
    st.title("📊 学生成绩分析与预测系统")
    st.divider()  

    st.subheader("一、项目概述")
    st.write("""
    本平台基于Streamlit开发，整合**数据可视化**与**机器学习**技术，为教育工作者和学生提供一站式成绩分析服务：
    - 核心数据来源：学生成绩数据集（含学号、性别、专业、学习时长、出勤率、期中/期末成绩等维度）
    - 技术栈：Streamlit（界面）、Pandas（数据处理）、Plotly（可视化）、Scikit-learn（预测模型）
    - 核心价值：快速识别成绩影响因素、直观展示学业表现、提前预测期末成绩，辅助教学决策与学习规划
    """)

    st.subheader("二、项目目标")
    goals = [
        "1. 分析影响因素：识别每周学习时长、出勤率、作业完成率等关键指标对成绩的影响",
        "2. 可视化展示：通过表格、柱状图、折线图等形式，直观呈现各专业学业表现",
        "3. 成绩预测：基于机器学习模型，输入学生信息即可预测期末成绩，支持提前干预"
    ]
    for goal in goals:
        st.write(goal)

    st.subheader("三、功能界面预览")
    st.write("以下为各功能界面的实际效果预览：")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("项目介绍.JPG", caption="项目介绍界面", use_container_width=True)
    with col2:
        st.image("专业成绩.JPG", caption="专业成绩分析界面", use_container_width=True)
    with col3:
        st.image("期末成绩预测.JPG", caption="期末成绩预测界面", use_container_width=True)

# ---------------------- 界面2：专业成绩分析 ----------------------
elif page == "专业成绩分析":
    st.title("📈 专业成绩多维度分析")
    st.divider()

    major_stats = df.groupby("专业").agg({
        "每周学习时长（小时）": "mean",
        "期中考试分数": "mean",
        "期末考试分数": "mean",
        "上课出勤率": "mean",
        "性别": lambda x: x.value_counts().to_dict()  
    }).round(2)

    st.subheader("1. 各专业核心指标统计")
    major_stats["男生人数"] = major_stats["性别"].apply(lambda x: x.get("男", 0))
    major_stats["女生人数"] = major_stats["性别"].apply(lambda x: x.get("女", 0))
    display_table = major_stats[["每周学习时长（小时）", "期中考试分数", "期末考试分数", "上课出勤率", "男生人数", "女生人数"]]
    st.dataframe(display_table, use_container_width=True)

    st.subheader("2. 各专业男女性别比例")
    gender_data = display_table[["男生人数", "女生人数"]].reset_index()
    gender_fig = px.bar(
        gender_data,
        x="专业",
        y=["男生人数", "女生人数"],
        barmode="group",
        title="各专业男女生人数对比",
        labels={"value": "人数", "专业": "专业名称"},
        color_discrete_map={"男生人数": "#1f77b4", "女生人数": "#ff7f0e"}
    )
    st.plotly_chart(gender_fig, use_container_width=True)

    st.subheader("3. 各专业期中/期末分数趋势")
    score_data = major_stats[["期中考试分数", "期末考试分数"]].reset_index()
    score_data_long = pd.melt(
        score_data,
        id_vars="专业",
        value_vars=["期中考试分数", "期末考试分数"],
        var_name="考试类型",
        value_name="平均分数"
    )
    score_fig = px.line(
        score_data_long,
        x="专业",
        y="平均分数",
        color="考试类型",
        markers=True,
        title="各专业期中/期末平均分数对比",
        labels={"平均分数": "平均分数（分）", "专业": "专业名称"}
    )
    st.plotly_chart(score_fig, use_container_width=True)

    st.subheader("4. 各专业平均上课出勤率")
    attendance_fig = px.bar(
        major_stats.reset_index(),
        x="专业",
        y="上课出勤率",
        title="各专业平均上课出勤率",
        labels={"上课出勤率": "平均出勤率", "专业": "专业名称"},
        color="专业",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    attendance_fig.update_traces(texttemplate="%{y:.1%}", textposition="outside")
    st.plotly_chart(attendance_fig, use_container_width=True)

    st.subheader("5. 大数据管理专业：出勤率与期末成绩关系")
    bigdata_df = df[df["专业"] == "大数据管理"]
    if len(bigdata_df) > 0:
        bigdata_fig = px.scatter(
            bigdata_df,
            x="上课出勤率",
            y="期末考试分数",
            title="大数据管理专业：出勤率与期末成绩分布",
            labels={"上课出勤率": "上课出勤率", "期末考试分数": "期末成绩（分）"},
            hover_data=["学号", "性别"],
            color="性别",
            size="每周学习时长（小时）",
            size_max=10
        )
        
        x = bigdata_df["上课出勤率"]
        y = bigdata_df["期末考试分数"]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        trend_x = np.linspace(x.min(), x.max(), 100)
        trend_y = intercept + slope * trend_x
        
        bigdata_fig.add_trace(
            go.Scatter(
                x=trend_x,
                y=trend_y,
                mode="lines",
                line=dict(color="#ff5733", dash="dash"),
                name="趋势线 (R²={:.2f})".format(r_value**2)
            )
        )
        
        st.plotly_chart(bigdata_fig, use_container_width=True)
    else:
        st.warning("未找到大数据管理专业的学生数据，请检查数据集中的专业名称是否正确")

# ---------------------- 界面3：期末成绩预测（滚动条版） ----------------------
elif page == "期末成绩预测":
    # 页面标题（简化，匹配图2）
    st.title("学生期末成绩预测")
    st.divider()

    # 顶部提示栏（匹配图2的浅蓝色提示框）
    st.info("请输入学生的学习信息，系统将基于机器学习模型预测期末成绩")

    # 输入区域布局（左列：学号/性别/专业/学习时长；右列：出勤率/期中分数/作业完成率）
    col1, col2 = st.columns([1, 1])
    with col1:
        student_id = st.text_input("学号", placeholder="例如：23333321")
        gender = st.selectbox("性别", ["男", "女"])
        major = st.selectbox("专业", majors)
        
        # 每周学习时长 → 滚动条（Slider）
        study_hours = st.slider(
            "每周学习时长（小时）",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            value=0.0,  # 默认值
            format="%.1f"
        )
    with col2:
        # 上课出勤率 → 滚动条（Slider）
        attendance = st.slider(
            "上课出勤率",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            value=0.0,  # 默认值
            format="%.2f"
        )
        
        # 期中考试分数 → 滚动条（Slider）
        midterm_score = st.slider(
            "期中考试分数",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            value=0.0,  # 默认值
            format="%.1f"
        )
        
        # 作业完成率 → 滚动条（Slider）
        homework_rate = st.slider(
            "作业完成率",
            min_value=0.0,
            max_value=1.0,
            step=0.01,
            value=0.0,  # 默认值
            format="%.2f"
        )

    # 红色预测按钮（匹配图2）
    predict_btn = st.button("预测期末成绩", type="primary")

    # 预测逻辑与结果展示（匹配图2的卡片+进度条+图片）
    if predict_btn:
        # 输入验证（优化提示，匹配图2）
        if study_hours <= 0 or attendance <= 0 or midterm_score <= 0 or homework_rate <= 0:
            st.error("请填写有效信息（学习时长、出勤率等不可为0）！")
        elif not student_id:
            st.error("请填写学号！")
        else:
            # 构造特征数据
            input_data = pd.DataFrame({
                "性别": [gender],
                "专业": [major],
                "每周学习时长（小时）": [study_hours],
                "上课出勤率": [attendance],
                "期中考试分数": [midterm_score],
                "作业完成率": [homework_rate]
            })

            # 模型预测
            predicted_score = model.predict(input_data)[0].round(2)

            # 结果展示（用默认主题的卡片样式，匹配图2）
            with st.container(border=True):  # 带边框的卡片，匹配图2
                st.subheader("预测结果")
                st.write(f"📊 {student_id} 同学的期末成绩预测为：**{predicted_score} 分**")
                # 分数进度条（匹配图2）
                st.progress(min(predicted_score / 100, 1.0))  

                # 加载本地及格/不及格图片（设置width缩小尺寸，比如300像素）
                if predicted_score >= 60:
                    # 设置width=300（可根据需求调整数值，比如200、350等）
                    st.image("及格.png", caption="恭喜！成绩及格", width=300)
                    st.success("✅ 成绩达标！建议保持当前学习节奏，巩固薄弱知识点~")
                else:
                    st.image("不及格.png", caption="加油！继续努力", width=300)
                    st.warning("⚠️ 建议增加学习时长、提高出勤率，优先完成作业提升成绩哦~")
