# 第8章/streamlit_predict_v2.py - 修复物种映射+特征列名问题
import streamlit as st
import pickle
import pandas as pd
import os
import chardet
import zipfile
import io
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

# ===================== 全局配置（适配实际数据集列名） =====================
DATA_PATH = "penguins-chinese.csv"  # 中文数据集路径
MODEL_PATH = "rfc_model.pkl"        # 模型保存路径
MAP_PATH = "output_uniques.pkl"     # 物种映射文件路径
ZIP_IMAGE_PATH = "images.zip"       # 图片压缩包路径（与代码同目录）
# 实际数据集必要列名（从报错信息中提取）
REQUIRED_COLS = [
    "企鹅栖息的岛屿", "性别", "喙的长度", "喙的深度", 
    "翅膀的长度", "身体质量", "企鹅的种类"
]
# 模型输入特征列名（适配实际分类特征）
FEATURE_NAMES = [
    "喙的长度", "喙的深度", "翅膀的长度", "身体质量",
    "企鹅栖息的岛屿_托托尔森岛", "企鹅栖息的岛屿_比斯科岛", "企鹅栖息的岛屿_德里姆岛",
    "性别_雌性", "性别_雄性"
]

# ===================== 核心辅助函数：读取ZIP内图片（适配zip根目录） =====================
def load_image_from_zip(zip_file_path, image_filename):
    """从zip压缩包根目录读取图片"""
    try:
        if not os.path.exists(zip_file_path):
            st.warning(f"❌ 图片压缩包 {zip_file_path} 未找到！")
            return None
        
        with zipfile.ZipFile(zip_file_path, 'r') as zf:
            if image_filename not in zf.namelist():
                st.warning(f"❌ zip内未找到图片：{image_filename}")
                st.info(f"zip内所有文件：{zf.namelist()[:5]}...")
                return None
            
            with zf.open(image_filename) as f:
                img_data = io.BytesIO(f.read())
                img = Image.open(img_data)
                return img
    except Exception as e:
        st.warning(f"⚠️ 读取图片失败：{str(e)}")
        return None

# ===================== 辅助函数：检测文件编码 =====================
def detect_encoding(file_path):
    """检测CSV文件编码，解决中文解码错误"""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
    return chardet.detect(raw_data)['encoding']

# ===================== 数据预处理与模型训练（适配实际列名） =====================
def load_preprocess_data():
    """加载实际数据集并预处理（修复物种映射）"""
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
        st.error("❌ 数据集清洗后无有效数据（全为缺失值）")
        st.stop()
    
    # 5. 分离特征（X）和标签（y）（用实际列名）
    X = df[["企鹅栖息的岛屿", "性别", "喙的长度", "喙的深度", "翅膀的长度", "身体质量"]]
    y = df["企鹅的种类"]
    
    # 6. 标签编码（确保物种索引与模型一致）
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    # 保存物种映射（用LabelEncoder的classes_，确保索引正确）
    species_map = {i: sp for i, sp in enumerate(label_encoder.classes_)}
    
    # 7. 分类特征独热编码（适配实际列名）
    cat_encoder = OneHotEncoder(sparse_output=False, drop=None)
    encoded_cats = cat_encoder.fit_transform(X[["企鹅栖息的岛屿", "性别"]])
    
    # 8. 构造编码后特征名（适配实际列名）
    encoded_names = []
    for i, feat in enumerate(["企鹅栖息的岛屿", "性别"]):
        for cat in cat_encoder.categories_[i]:
            encoded_names.append(f"{feat}_{cat}")
    
    # 9. 合并数值特征与编码特征
    numeric_feat = X[["喙的长度", "喙的深度", "翅膀的长度", "身体质量"]].reset_index(drop=True)
    encoded_df = pd.DataFrame(encoded_cats, columns=encoded_names)
    X_processed = pd.concat([numeric_feat, encoded_df], axis=1)
    
    # 10. 补全特征列（确保与FEATURE_NAMES一致）
    for col in FEATURE_NAMES:
        if col not in X_processed.columns:
            X_processed[col] = 0.0
    X_processed = X_processed[FEATURE_NAMES]
    
    return X_processed, y_encoded, species_map, cat_encoder, label_encoder

def train_model(force_retrain=False):
    """
    训练随机森林模型并保存
    :param force_retrain: 是否强制重新训练（删除旧模型）
    """
    # 强制删除旧模型
    if force_retrain:
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        if os.path.exists(MAP_PATH):
            os.remove(MAP_PATH)
    
    # 已有模型且不强制重训则直接返回
    if os.path.exists(MODEL_PATH) and os.path.exists(MAP_PATH) and not force_retrain:
        return
    
    # 加载预处理数据
    X, y, species_map, _, _ = load_preprocess_data()
    
    # 划分训练集
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 训练模型
    rfc = RandomForestClassifier(n_estimators=100, random_state=42)
    rfc.fit(X_train, y_train)
    
    # 保存模型和物种映射
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(rfc, f)
    with open(MAP_PATH, 'wb') as f:
        pickle.dump(species_map, f)
    
    st.success("✅ 模型训练完成！已生成rfc_model.pkl和output_uniques.pkl")

# ===================== 页面功能 =====================
def intro_page():
    """简介页面（适配实际列名）"""
    st.title("企鹅分类器 🐧")
    st.header("数据集介绍（中文版）")
    st.markdown("""**帕尔默群岛企鹅中文数据集包含344条观测记录，涵盖3种南极企鹅：
    阿德利企鹅、巴布亚企鹅和帽带企鹅。数据记录了企鹅的栖息岛屿、性别、
    喙长度/深度、翅膀长度及身体质量等关键特征，适用于机器学习分类练习和数据可视化分析。**""")
    
    st.header("三种企鹅特征差异")
    st.markdown("""
    - **阿德利企鹅**：体型较小，喙短而钝，主要栖息于托托尔森岛；
    - **巴布亚企鹅**：体型较大，喙尖且长，翅膀长度最长；
    - **帽带企鹅**：头部有黑色条纹（似帽带），喙中等长度。
    """)
    
    # 读取zip根目录的penguins.png
    penguin_img = load_image_from_zip(ZIP_IMAGE_PATH, "penguins.png")
    if penguin_img:
        st.image(penguin_img, caption="三种企鹅卡通图")
    else:
        st.info("⚠️ 未加载到企鹅示意图，可检查images.zip内是否有penguins.png")

def predict_page():
    """预测页面（修复物种映射+特征列名问题）"""
    st.header("企鹅物种预测")
    st.markdown("""输入以下6项企鹅特征，系统将基于随机森林模型预测其物种：
    - 注：特征值需符合实际范围（如喙长度30-60mm，身体质量2700-6300g）""")
    
    # 3:1:2列布局
    col_form, col1, col_logo = st.columns([3, 1, 2])
    with col_form:
        with st.form('user_inputs'):
            # 中文输入表单（与实际分类值一致）
            island = st.selectbox('栖息岛屿', options=['托托尔森岛', '比斯科岛', '德里姆岛'])
            sex = st.selectbox('性别', options=['雌性', '雄性'])
            bill_length = st.number_input('喙的长度(毫米)', min_value=30.0, max_value=60.0, value=45.0)
            bill_depth = st.number_input('喙的深度(毫米)', min_value=15.0, max_value=25.0, value=20.0)
            flipper_length = st.number_input('翅膀的长度(毫米)', min_value=170.0, max_value=240.0, value=200.0)
            body_mass = st.number_input('身体质量(克)', min_value=2700.0, max_value=6300.0, value=4000.0)
            submitted = st.form_submit_button('预测物种', type='primary')

            # 1. 初始化特征向量（与FEATURE_NAMES对齐，浮点型）
            feature_vec = [0.0] * len(FEATURE_NAMES)
            # 填充数值特征（适配实际列名）
            feature_vec[FEATURE_NAMES.index("喙的长度")] = bill_length
            feature_vec[FEATURE_NAMES.index("喙的深度")] = bill_depth
            feature_vec[FEATURE_NAMES.index("翅膀的长度")] = flipper_length
            feature_vec[FEATURE_NAMES.index("身体质量")] = body_mass
            # 填充分类特征（独热编码，适配实际列名）
            feature_vec[FEATURE_NAMES.index(f"企鹅栖息的岛屿_{island}")] = 1.0
            feature_vec[FEATURE_NAMES.index(f"性别_{sex}")] = 1.0

            # 2. 预测逻辑
            pred_species = ""  # 初始化预测结果
            if submitted:
                try:
                    # 强制重新训练模型（确保用最新数据）
                    train_model(force_retrain=True)

                    # 加载模型和物种映射
                    with open(MODEL_PATH, 'rb') as f:
                        rfc_model = pickle.load(f)
                    with open(MAP_PATH, 'rb') as f:
                        species_map = pickle.load(f)

                    # 格式化输入数据（确保列名、类型匹配）
                    input_df = pd.DataFrame(
                        data=[feature_vec],
                        columns=FEATURE_NAMES,
                        dtype=float
                    )

                    # 预测（返回编码后的物种索引）
                    pred_idx = rfc_model.predict(input_df)[0]
                    # 映射索引到物种名（确保species_map的键是整数）
                    pred_species = species_map.get(int(pred_idx), "未知物种")

                    # 显示结果
                    if pred_species != "未知物种":
                        st.success(f"🎉 预测结果：该企鹅为 **{pred_species}**")
                    else:
                        st.warning("⚠️ 无法识别该企鹅物种，请检查输入特征是否合理")

                # 细化异常捕获
                except FileNotFoundError as e:
                    st.error(f"❌ 模型文件缺失：{str(e)}")
                    st.info("正在自动重新训练模型...")
                    train_model(force_retrain=True)
                except KeyError as e:
                    st.error(f"❌ 物种映射不匹配：{str(e)}")
                    st.info("已重新训练模型，再次点击预测按钮即可")
                    train_model(force_retrain=True)
                except ValueError as e:
                    st.error(f"❌ 输入值错误：{str(e)}")
                    st.info("请确保所有输入值在合理范围内（如身体质量2700-6300g）")
                except Exception as e:
                    st.error(f"❌ 预测出错：{str(e)}")
                    st.info("已自动修复模型，请再次点击预测按钮")
                    train_model(force_retrain=True)

    # 右侧显示图片（从zip根目录读取）
    with col_logo:
        if not submitted:
            # 读取zip根目录的logo图片
            logo_img = load_image_from_zip(ZIP_IMAGE_PATH, "rigth_logo.png")
            if logo_img:
                st.image(logo_img, width=300, caption="企鹅分类器")
            else:
                st.info("⚠️ 未加载到Logo图片，可检查images.zip内是否有rigth_logo.png")
        else:
            # 预测后读取对应物种图片
            if pred_species and pred_species != "未知物种":
                species_img = load_image_from_zip(ZIP_IMAGE_PATH, f"{pred_species}.png")
                if species_img:
                    st.image(species_img, width=300, caption=f"{pred_species}")
                else:
                    st.info(f"⚠️ 未加载到{pred_species}的图片，可检查images.zip内是否有{pred_species}.png")
            else:
                st.info("⚠️ 暂无有效预测结果，无法加载物种图片")

# ===================== 主程序 =====================
def main():
    # 页面基础配置
    st.set_page_config(
        page_title="企鹅分类器（中文数据集版）",
        page_icon="🐧",
        layout="wide"
    )

    # 侧边栏导航（读取zip根目录的logo）
    with st.sidebar:
        # 读取zip根目录的logo图片
        sidebar_logo = load_image_from_zip(ZIP_IMAGE_PATH, "rigth_logo.png")
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
