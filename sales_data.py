#第10章/final_app.PY
import pandas as pd
import streamlit as st
import plotly.express as px

def get_dataframe_from_excel():
    #pd.read_excel()函数用于读取Excel文件的数据
    #*supermarket_sales.xlsx'表示Excel文件的路径及名称
    #*sheet_name='销售数据'表示读取Excel中名为"销售数据"的工作表的数据
    #*skiprows=1表示跳过Excel表中的第1行，因为第1行是标题
    #*index_col='订单号'表示将"订单号"这一列作为返回的数据框的索引
    #最后将读取到的数据框赋值给变量df
    df = pd.read_excel('supermarket_sales.xlsx',
                       sheet_name='销售数据',
                       skiprows=1,
                       index_col='订单号'
                       )
    #df['时间']取出原有的'时间'这一列，其中包含交易的完整时间字符串，如'10:25:30'
    #pd.to_datetime将'时间'列转换成datetime类型
    #*format="%H:%M:%S"指定原有时间字符串的格式
    #*.dt.hour表示从转换后的数据框取出小时数作为新列
    #最后赋值给sale_df['小时数']，得到包含交易小时的新列
    df['小时数'] = pd.to_datetime(df["时间"], format="%H:%M:%S").dt.hour
    return df

def add_sidebar_func(df):
    #创建侧边栏
    with st.sidebar:
        #添加侧边栏标题
        st.header("请筛选数据：")
        #求"城市"列去重后的值，赋值给city_unique
        city_unique = df["城市"].unique()
        city = st.multiselect(
            "请选择城市：",
            options=city_unique,  #选项为city_unique
            default=city_unique,  #默认选中所有城市
        )
        #求"顾客类型"列去重后的值，赋值给customer_type_unique
        customer_type_unique = df["顾客类型"].unique()
        customer_type = st.multiselect(
            "请选择顾客类型：",
            options=customer_type_unique,  #选项为customer_type_unique
            default=customer_type_unique,  #默认选中所有顾客类型
        )
        #求"性别"列去重后的值，赋值给gender_unique
        gender_unique = df["性别"].unique()
        gender = st.multiselect(
            "请选择性别：",
            options=gender_unique,  #选项为gender_unique
            default=gender_unique,  #默认选中所有性别
        )
        #通过query筛选数据（@变量表示引用Streamlit组件的值）
        df_selection = df.query(
            "城市 == @city & 顾客类型 == @customer_type & 性别 == @gender"
        )
    return df_selection

def product_line_chart(df):
    #按"产品类型"分组，计算"总价"列的和并按总价排序
    sales_by_product_line = (
        df.groupby(by=["产品类型"])[["总价"]].sum().sort_values(by="总价")
    )
    #生成横向条形图（按产品类型的销售额）
    fig_product_sales = px.bar(
        sales_by_product_line,
        x="总价",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>按产品类型划分的销售额</b>",
    )
    return fig_product_sales

def hour_chart(df):
    #按"小时数"分组，计算"总价"列的和
    sales_by_hour = (
        df.groupby(by=["小时数"])[["总价"]].sum()
    )
    #生成条形图（按小时数的销售额）
    fig_hour_sales = px.bar(
        sales_by_hour,
        x=sales_by_hour.index,
        y="总价",
        title="<b>按小时数划分的销售额</b>",
    )
    return fig_hour_sales

def main_page_demo(df):
    """主界面函数"""
    #设置页面标题
    st.title('📊销售仪表板')
    #创建3列容器（用于显示关键指标）
    left_key_col, middle_key_col, right_key_col = st.columns(3)

    #计算总销售额（取整）
    total_sales = int(df["总价"].sum())
    #计算平均评分（保留1位小数）
    average_rating = round(df["评分"].mean(), 1)
    #将评分转换为星级显示
    star_rating = ":star:" * int(round(average_rating, 0))
    #计算每单平均销售额（保留2位小数）
    average_sale_by_transaction = round(df["总价"].mean(), 2)

    with left_key_col:
        st.subheader("总销售额：")
        st.subheader(f"RMB ¥ {total_sales:,}")
    with middle_key_col:
        st.subheader("顾客评分的平均值：")
        st.subheader(f"{average_rating} {star_rating}")
    with right_key_col:
        st.subheader("每单的平均销售额：")
        st.subheader(f"RMB ¥ {average_sale_by_transaction}")

    st.divider()  #添加水平分割线
    #创建2列容器（用于显示图表）
    left_chart_col, right_chart_col = st.columns(2)
    with left_chart_col:
        hour_fig = hour_chart(df)
        st.plotly_chart(hour_fig, use_container_width=True)
    with right_chart_col:
        product_fig = product_line_chart(df)
        st.plotly_chart(product_fig, use_container_width=True)

def run_app():
    """启动应用"""
    #设置页面配置（标题、图标、宽布局）
    st.set_page_config(page_title="销售仪表板",
                       page_icon="📊",
                       layout="wide"
                       )
    #读取Excel数据
    sale_df = get_dataframe_from_excel()
    #通过侧边栏筛选数据
    df_selection = add_sidebar_func(sale_df)
    #渲染主界面
    main_page_demo(df_selection)

#标准Python程序入口
if __name__ == "__main__":
    run_app()
