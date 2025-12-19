# 第8章/streamlit_predict_v2.py - 适配中文数据集penguins-chinese.csv
import streamlit as st
import pickle
import pandas as pd
import os
import chardet
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# ===================== 全局配置（适配中文数据集） =====================
DATA_PATH = "penguins-chinese.csv"  # 中文数据集路径
MODEL_PATH = "rfc_model.pkl"        # 模型保存路径
MAP_PATH = "output_uniques.pkl"     # 物种映射文件路径
# 中文数据集必要列名（已从CSV读取确认）
REQUIRED_COLS = ["岛屿", "性别", "喙长度(mm)", "喙深度(mm)", "鳍长度(mm)", "体重(g)", "物种"]
# 模型输入特征列名（中文编码后）
FEATURE_NAMES = [
    "喙长度(mm)", "喙深度(mm)", "鳍长度(mm)", "体重(g)",
    "岛屿_托托尔森岛", "岛屿_比斯科岛", "岛屿_德里姆岛",
    "性别_雌性", "性别_雄性"
]

# ===================== 辅助函数：检测文件编码 =====================
def detect_encoding(file_path):
    """检测CSV文件编码，解决中文解码错误"""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
    return chardet.detect(raw_data)['encoding']

# ===================== 数据预处理与模型训练 =====================
def load_preprocess_data():
    """加载中文数据集并预处理"""
    # 1. 检查文件是否存在
    if not os.path.exists(DATA_PATH):
        st.error(f"❌ 未找到数据集：{DATA_PATH}，请放在代码同一目录！")
        st.stop()
    
    # 2. 读取中文CSV（适配编码）
    try:
        df = pd.read_csv(DATA_PATH, encoding='gbk')
    except UnicodeDecodeError:
        enc = detect_encoding(DATA_PATH)
        st.warning(f"⚠️ 用检测到的编码{enc}读取文件")
        df = pd.read_csv(DATA_PATH, encoding=enc)
    
    # 3. 检查必要列
    missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing_cols:
        st.error(f"❌ 数据集缺少列：{missing_cols}")
        st.error(f"当前列名：{list(df.columns)}")
        st.stop()
    
    # 4. 处理缺失值
    df = df.dropna(subset=REQUIRED_COLS)
    if len(df) == 0:
        st.error("❌ 数据集无有效数据（全为缺失值）")
        st.stop()
    
    # 5. 分离特征（X）和标签（y）
    X = df[["岛屿", "性别", "喙长度(mm)", "喙深度(mm)", "鳍长度(mm)", "体重(g)"]]
    y = df["物种"]
    
    # 6. 分类特征独热编码（中文值）
    cat_encoder = OneHotEncoder(sparse_output=False, drop=None)
    encoded_cats = cat_encoder.fit_transform(X[["岛屿", "性别"]])
    
    # 7. 构造编码后特征名
    encoded_names = []
    for i, feat in enumerate(["岛屿", "性别"]):
        for cat in cat_encoder.categories_[i]:
            encoded_names.append(f"{feat}_{cat}")
    
    # 8. 合并数值特征与编码特征
    numeric_feat = X[["喙长度(mm)", "喙深度(mm)", "鳍长度(mm)", "体重(g)"]].reset_index(drop=True)
    encoded_df = pd.DataFrame(encoded_cats, columns=encoded_names)
    X_processed = pd.concat([numeric_feat, encoded_df], axis=1)
    
    # 9. 补全特征列（确保与FEATURE_NAMES一致）
    for col in FEATURE_NAMES:
        if col not in X_processed.columns:
            X_processed[col] = 0
    X_processed = X_processed[FEATURE_NAMES]
    
    # 10. 生成物种映射（用于预测结果显示）
    species_map = {i: sp for i, sp in enumerate(y.unique())}
    return X_processed, y, species_map, cat_encoder

def train_model():
    """训练随机森林模型并保存（无模型时自动执行）"""
    if os.path.exists(MODEL_PATH) and os.path.exists(MAP_PATH):
        return
    
    # 加载预处理数据
    X, y, species_map, _ = load_preprocess_data()
    
    # 划分训练集
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 训练模型
    rfc = RandomForestClassifier(n_estimators=100, random_state=42)
    rfc.fit(X_train, y_train)
    
    # 保存模型和映射
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(rfc, f)
    with open(MAP_PATH, 'wb') as f:
        pickle.dump(species_map, f)
    
    st.success("✅ 模型训练完成！已生成rfc_model.pkl和output_uniques.pkl")

# ===================== 页面功能 =====================
def intro_page():
    """简介页面（适配中文数据集说明）"""
    st.title("企鹅分类器 🐧")
    st.header("数据集介绍（中文版）")
    st.markdown("""**帕尔默群岛企鹅中文数据集包含344条观测记录，涵盖3种南极企鹅：
    阿德利企鹅、巴布亚企鹅和帽带企鹅。数据记录了企鹅的栖息岛屿、性别、
    喙长度/深度、鳍长度及体重等关键特征，适用于机器学习分类练习和数据可视化分析。**""")
    
    st.header("三种企鹅特征差异")
    st.markdown("""
    - **阿德利企鹅**：体型较小，喙短而钝，主要栖息于托托尔森岛；
    - **巴布亚企鹅**：体型较大，喙尖且长，鳍长度最长；
    - **帽带企鹅**：头部有黑色条纹（似帽带），喙中等长度。
    """)
    
    # 若没有images文件夹，可注释下方图片代码，避免报错
    try:
        st.image('images/penguins.png', caption="三种企鹅卡通图")
    except:
        st.info("⚠️ 未找到images/penguins.png，可自行添加图片文件展示企鹅示意图")

def predict_page():
    """预测页面（全中文交互）"""
    st.header("企鹅物种预测")
    st.markdown("""输入以下6项企鹅特征，系统将基于随机森林模型预测其物种：
    - 注：特征值需符合实际范围（如喙长度30-60mm，体重2700-6300g）""")
    
    # 3:1:2列布局
    col_form, col1, col_logo = st.columns([3, 1, 2])
    with col_form:
        with st.form('user_inputs'):
            # 中文输入表单（与数据集分类值一致）
            island = st.selectbox('栖息岛屿', options=['托托尔森岛', '比斯科岛', '德里姆岛'])
            sex = st.selectbox('性别', options=['雌性', '雄性'])
            bill_length = st.number_input('喙长度(毫米)', min_value=30.0, max_value=60.0, value=45.0)
            bill_depth = st.number_input('喙深度(毫米)', min_value=15.0, max_value=25.0, value=20.0)
            flipper_length = st.number_input('鳍长度(毫米)', min_value=170.0, max_value=240.0, value=200.0)
            body_mass = st.number_input('体重(克)', min_value=2700.0, max_value=6300.0, value=4000.0)
            submitted = st.form_submit_button('预测物种', type='primary')

            # 1. 初始化特征向量（与FEATURE_NAMES对齐）
            feature_vec = [0] * len(FEATURE_NAMES)
            # 填充数值特征
            feature_vec[FEATURE_NAMES.index("喙长度(mm)")] = bill_length
            feature_vec[FEATURE_NAMES.index("喙深度(mm)")] = bill_depth
            feature_vec[FEATURE_NAMES.index("鳍长度(mm)")] = flipper_length
            feature_vec[FEATURE_NAMES.index("体重(g)")] = body_mass
            # 填充分类特征（独热编码）
            feature_vec[FEATURE_NAMES.index(f"岛屿_{island}")] = 1
            feature_vec[FEATURE_NAMES.index(f"性别_{sex}")] = 1

            # 2. 加载模型（无模型则自动训练）
            if not (os.path.exists(MODEL_PATH) and os.path.exists(MAP_PATH)):
                with st.spinner("首次使用，正在训练模型...（约5秒）"):
                    train_model()

            # 3. 预测逻辑
            if submitted:
                try:
                    # 加载模型和物种映射
                    with open(MODEL_PATH, 'rb') as f:
                        rfc_model = pickle.load(f)
                    with open(MAP_PATH, 'rb') as f:
                        species_map = pickle.load(f)

                    # 格式化输入数据
                    input_df = pd.DataFrame([feature_vec], columns=FEATURE_NAMES)
                    # 预测（返回物种索引，映射为中文名称）
                    pred_idx = rfc_model.predict(input_df)[0]
                    pred_species = species_map[pred_idx]

                    # 显示结果
                    st.success(f"🎉 预测结果：该企鹅为 **{pred_species}**")

                except Exception as e:
                    st.error(f"❌ 预测出错：{str(e)}")
                    st.info("建议：删除rfc_model.pkl和output_uniques.pkl后重新运行，重新训练模型")

    # 右侧显示图片（无图片时显示提示）
    with col_logo:
        if not submitted:
            try:
                st.image('images/rigth_logo.png', width=300, caption="企鹅分类器")
            except:
                st.info("⚠️ 未找到images/rigth_logo.png，可添加Logo图片")
        else:
            # 预测后显示对应物种图片（需提前准备图片，命名为物种名.png）
            try:
                st.image(f'images/{pred_species}.png', width=300, caption=f"{pred_species}")
            except:
                st.info(f"⚠️ 未找到{pred_species}的图片，可添加images/{pred_species}.png")

# ===================== 主程序 =====================
def main():
    # 页面基础配置
    st.set_page_config(
        page_title="企鹅分类器（中文数据集版）",
        page_icon="🐧",
        layout="wide"
    )

    # 侧边栏导航
    with st.sidebar:
        # 无logo图片时注释下方代码
        try:
            st.image('images/rigth_logo.png', width=100)
        except:
            pass
        st.title('功能导航')
        page = st.selectbox(
            "选择页面", 
            ["简介页面", "预测分类页面"], 
            label_visibility='collapsed'
        )

    # 页面路由
    if page == "简介页面":
        intro_page()
    else:
        predict_page()

if __name__ == "__main__":
    main()
