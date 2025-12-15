import streamlit as st
from datetime import date, time

# 页面配置
st.set_page_config(page_title="个人简历生成器",page_icon='👩‍🎓', layout="wide")
st.header("个人简历生成器")

# 分栏：左1份（表单）、右2份（预览）
col1, col2 = st.columns([1, 2], gap="large")  # 增加gap让左右栏更分明


#左栏：信息表单（紧凑布局）
with col1:
    with st.form("info_form", clear_on_submit=False):
        st.subheader("个人信息表单")
        
        # 原有字段（紧凑排列）
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
        
        # 照片上传
        photo = st.file_uploader("选择照片", type=["jpg", "png", "jpeg"])
        
        # 表单提交按钮
        submit_btn = st.form_submit_button("更新简历")


# 右栏：预览区域
with col2:
    st.subheader("简历实时预览")
       # 展示照片
    if submit_btn and photo:
        #st.markdown("---")
        #st.subheader("个人照片")
        st.image(photo, width=200, caption="本人照片")
        
    # 右栏内部分2列
    #左列
    info_col1, info_col2 = st.columns(2)
    with info_col1:
        st.write(f"姓名:{name}")
        st.write(f"职位: {position}")
        st.write(f"电话: {phone if phone else ''}")
        st.write(f"邮箱: {email if email else ''}")
        st.write(f"出生日期: {birth_date}")
    #右列
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
    
 
