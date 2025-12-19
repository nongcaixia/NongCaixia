# 第8章/streamlit_predict_v2.py - 直接读取根目录图片（适配你的文件结构）
import streamlit as st
import pickle
import pandas as pd
import os
import chardet
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# ===================== 全局配置（适配根目录图片） =====================
DATA_PATH = "penguins-chinese.csv"  # 中文数据集路径
MODEL_PATH = "rfc_model.pkl"        # 模型保存路径
MAP_PATH = "output_uniques.pkl"     # 物种映射文件路径
# 实际数据集必要列名
REQUIRED_COLS = [
    "企鹅栖息的岛屿", "性别", "喙的长度", "喙的深度", 
    "翅膀的长度", "身体质量", "企鹅的种类"
]
# 模型输入特征列名
FEATURE_NAMES = [
    "喙的长度", "喙的深度", "翅膀的长度", "身体质量",
    "企鹅栖息的岛屿_托托尔森岛", "企鹅栖息的岛屿_比斯科岛", "企鹅栖息的岛屿_德里姆岛",
    "性别_雌性", "性别_雄性"
]

# ===================== 核心辅助函数：直接读取根目录图片 =====================
def load_local_image(image_filename):
    """读取项目根目录下的图片（适配你的文件结构）"""
    try:
        # 图片直接在根目录，路径就是文件名本身
        if os.path.exists(image_filename):
            return Image.open(image_filename)
        else:
            st.warning(f"❌ 未找到图片：{image_filename}（请确认文件在项目根目录）")
            return None
    except Exception as e:
        st.warning(f"⚠️ 读取图片失败：{str(e)}")
        return None

# ===================== 辅助函数：检测文件编码 =====================
def detect_encoding(file_path):
    """检测CSV文件编码"""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
    return chardet.detect(raw_data)['encoding']

# ===================== 数据预处理与模型训练 =====================
def load_preprocess_data():
    """加载数据集并预处理"""
    if not os.path.exists(DATA_PATH):
        st.error(f"❌ 未找到数据集：{DATA_PATH}（请放在项目根目录）")
        st.stop()
    
    # 读取中文CSV（适配编码）
    try:
        df = pd.read_csv(DATA_PATH, encoding='gbk')
    except UnicodeDecodeError:
        enc = detect_encoding(DATA_PATH)
        st.warning(f"⚠️ 用编码{enc}读取文件")
        df = pd.read_csv(DATA_PATH, encoding=enc)
    
    # 检查必要列
    missing_cols = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing_cols:
        st.error(f"❌ 数据集缺少列：{missing_cols}")
        st.stop()
    
    # 处理缺失值
    df = df.dropna(subset=REQUIRED_COLS)
    if len(df) == 0:
        st.error("❌ 数据集无有效数据")
        st.stop()
    
    # 分离特征和标签
    X = df[["企鹅栖息的岛屿", "性别", "喙的长度", "喙的深度", "翅膀的长度", "身体质量"]]
    y = df["企鹅的种类"]
    
    # 标签编码
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    species_map = {i: sp for i, sp in enumerate(label_encoder.classes_)}
    
    # 独热编码分类特征
    cat_encoder = OneHotEncoder(sparse_output=False, drop=None)
    encoded_cats = cat_encoder.fit_transform(X[["企鹅栖息的岛屿", "性别"]])
    
    # 构造编码特征名
    encoded_names = []
    for i, feat in enumerate(["企鹅栖息的岛屿", "性别"]):
        for cat in cat_encoder.categories_[i]:
            encoded_names.append(f"{feat}_{cat}")
    
    # 合并特征
    numeric_feat = X[["喙的长度", "喙的深度", "翅膀的长度", "身体质量"]].reset_index(drop=True)
    encoded_df = pd.DataFrame(encoded_cats, columns=encoded_names)
    X_processed = pd.concat([numeric_feat, encoded_df], axis=1)
    
    # 补全特征列
    for col in FEATURE_NAMES:
        if col not in X_processed.columns:
            X_processed[col] = 0.0
    X_processed = X_processed[FEATURE_NAMES]
    
    return X_processed, y_encoded, species_map, cat_encoder, label_encoder

def train_model(force_retrain=False):
    """训练并保存模型"""
    if force_retrain:
        # 强制删除旧模型
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        if os.path.exists(MAP_PATH):
            os.remove(MAP_PATH)
    
    # 已有模型则跳过
    if os.path.exists(MODEL_PATH) and os.path.exists(MAP_PATH) and not force_retrain:
        return
    
    # 加载数据并训练
    X, y, species_map, _, _ = load_preprocess_data()
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    rfc = RandomForestClassifier(n_estimators=100, random_state=42)
    rfc.fit(X_train, y_train)
    
    # 保存模型
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(rfc, f)
    with open(MAP_PATH, 'wb') as f:
        pickle.dump(species_map, f)
    
    st.success("✅ 模型训练完成！")

# ===================== 页面功能（直接读取根目录图片） =====================
def intro_page():
    """简介页面"""
    st.title("企鹅分类器 🐧")
    st.header("数据集介绍（中文版）")
    st.markdown("""**帕尔默群岛企鹅中文数据集包含344条观测记录，涵盖3种南极企鹅：
    阿德利企鹅、巴布亚企鹅和帽带企鹅。**""")
    
    st.header("三种企鹅特征差异")
    st.markdown("""
    - **阿德利企鹅**：体型较小，喙短而钝；
    - **巴布亚企鹅**：体型较大，喙尖且长；
    - **帽带企鹅**：头部有黑色条纹，喙中等长度。
    """)
    
    # 读取根目录的「penguins.png」（你的文件里的图片）
    penguin_img = load_local_image("penguins.png")
    if penguin_img:
        st.image(penguin_img, caption="三种企鹅卡通图")
    else:
        st.info("⚠️ 未加载到企鹅示意图")

def predict_page():
    """预测页面（适配根目录图片）"""
    st.header("企鹅物种预测")
    st.markdown("""输入企鹅特征，系统将预测其物种：
    - 注：特征值需符合实际范围（如喙长度30-60mm，身体质量2700-6300g）""")
    
    # 布局
    col_form, col1, col_logo = st.columns([3, 1, 2])
    with col_form:
        with st.form('user_inputs'):
            # 输入表单
            island = st.selectbox('栖息岛屿', options=['托托尔森岛', '比斯科岛', '德里姆岛'])
            sex = st.selectbox('性别', options=['雌性', '雄性'])
            bill_length = st.number_input('喙的长度(毫米)', min_value=30.0, max_value=60.0, value=45.0)
            bill_depth = st.number_input('喙的深度(毫米)', min_value=15.0, max_value=25.0, value=20.0)
            flipper_length = st.number_input('翅膀的长度(毫米)', min_value=170.0, max_value=240.0, value=200.0)
            body_mass = st.number_input('身体质量(克)', min_value=2700.0, max_value=6300.0, value=4000.0)
            submitted = st.form_submit_button('预测物种', type='primary')

            # 初始化特征向量
            feature_vec = [0.0] * len(FEATURE_NAMES)
            # 填充数值特征
            feature_vec[FEATURE_NAMES.index("喙的长度")] = bill_length
            feature_vec[FEATURE_NAMES.index("喙的深度")] = bill_depth
            feature_vec[FEATURE_NAMES.index("翅膀的长度")] = flipper_length
            feature_vec[FEATURE_NAMES.index("身体质量")] = body_mass
            # 填充分类特征
            feature_vec[FEATURE_NAMES.index(f"企鹅栖息的岛屿_{island}")] = 1.0
            feature_vec[FEATURE_NAMES.index(f"性别_{sex}")] = 1.0

            # 预测逻辑
            pred_species = ""
            if submitted:
                try:
                    train_model(force_retrain=True)

                    # 加载模型
                    with open(MODEL_PATH, 'rb') as f:
                        rfc_model = pickle.load(f)
                    with open(MAP_PATH, 'rb') as f:
                        species_map = pickle.load(f)

                    # 预测
                    input_df = pd.DataFrame([feature_vec], columns=FEATURE_NAMES, dtype=float)
                    pred_idx = rfc_model.predict(input_df)[0]
                    pred_species = species_map.get(int(pred_idx), "未知物种")

                    # 显示结果
                    if pred_species != "未知物种":
                        st.success(f"🎉 预测结果：该企鹅为 **{pred_species}**")
                    else:
                        st.warning("⚠️ 无法识别该企鹅物种")

                except Exception as e:
                    st.error(f"❌ 预测出错：{str(e)}")
                    st.info("已自动重新训练模型，请再次点击预测")
                    train_model(force_retrain=True)

    # 右侧图片区域（直接读取根目录图片）
    with col_logo:
        if not submitted:
            # 读取根目录的「rigth_logo.png」（你的文件里的logo）
            logo_img = load_local_image("rigth_logo.png")
            if logo_img:
                st.image(logo_img, width=300, caption="企鹅分类器")
            else:
                st.info("⚠️ 未加载到Logo图片")
        else:
            # 读取根目录的物种图片（你的文件里的：阿德利企鹅.png、巴布亚企鹅.png、帽带企鹅.png）
            if pred_species and pred_species != "未知物种":
                species_img = load_local_image(f"{pred_species}.png")
                if species_img:
                    st.image(species_img, width=300, caption=f"{pred_species}")
                else:
                    st.info(f"⚠️ 未加载到{pred_species}的图片")
            else:
                st.info("⚠️ 暂无有效预测结果")

# ===================== 主程序 =====================
def main():
    st.set_page_config(
        page_title="企鹅分类器（中文数据集版）",
        page_icon="🐧",
        layout="wide"
    )

    # 侧边栏
    with st.sidebar:
        # 读取根目录的Logo
        sidebar_logo = load_local_image("rigth_logo.png")
        if sidebar_logo:
            st.image(sidebar_logo, width=100)
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
