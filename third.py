# 医疗费用预测应用 - 适配中文列名的insurance-chinese.csv数据集
import streamlit as st
import pickle
import pandas as pd
import os
import chardet  # 用于检测文件编码
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# ===================== 全局配置（适配中文列名/分类值） =====================
DATA_PATH = "insurance-chinese.csv"  # 与上传文件一致
MODEL_PATH = "rf_insurance_model.pkl"  # 模型保存路径
# 实际数据集分类特征的中文唯一值（适配CSV实际内容）
SEX_VALUES = ["女性", "男性"]  # 性别列实际值
SMOKER_VALUES = ["是", "否"]    # 是否吸烟列实际值
REGION_VALUES = ["东南部", "东北部", "西北部", "西南部"]  # 区域列实际值
# 最终模型输入特征列名（中文编码后，与预处理严格对齐）
FEATURE_NAMES = [
    "年龄", "BMI", "子女数量",
    "性别_女性", "性别_男性",
    "是否吸烟_否", "是否吸烟_是",
    "区域_东南部", "区域_东北部", "区域_西北部", "区域_西南部"
]

# ===================== 辅助函数：检测文件编码 =====================
def detect_file_encoding(file_path):
    """检测文件的实际编码，解决解码错误"""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # 读取前10000字节检测
    result = chardet.detect(raw_data)
    return result['encoding']

# ===================== 数据预处理与模型训练（全中文适配） =====================
def load_and_preprocess_data():
    """加载并预处理中文列名的insurance-chinese.csv数据"""
    # 1. 检查文件是否存在
    if not os.path.exists(DATA_PATH):
        st.error(f"❌ 未找到数据集文件：{DATA_PATH}")
        st.error("请确认文件是否放在代码同一目录下，且文件名正确！")
        st.stop()
    
    # 2. 检测编码并读取CSV（解决UnicodeDecodeError）
    try:
        # 先尝试GBK（中文Windows默认编码）
        df = pd.read_csv(DATA_PATH, encoding='gbk')
    except UnicodeDecodeError:
        try:
            # 尝试UTF-8-SIG（带BOM的UTF-8）
            df = pd.read_csv(DATA_PATH, encoding='utf-8-sig')
        except UnicodeDecodeError:
            # 自动检测编码
            enc = detect_file_encoding(DATA_PATH)
            st.warning(f"⚠️ 自动检测到文件编码：{enc}，尝试用该编码读取")
            df = pd.read_csv(DATA_PATH, encoding=enc)
    
    # 3. 检查必要列是否存在（中文列名）
    required_cols = ["年龄", "性别", "BMI", "子女数量", "是否吸烟", "区域", "医疗费用"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"❌ 数据集缺少必要列：{missing_cols}")
        st.error(f"当前数据集列名：{list(df.columns)}")
        st.stop()
    
    # 4. 数据清洗：处理可能的缺失值
    df = df.dropna(subset=required_cols)
    if len(df) == 0:
        st.error("❌ 数据集清洗后无有效数据（可能全是缺失值）")
        st.stop()
    
    # 5. 分离特征（X）和标签（y）（中文列名）
    X = df[["年龄", "性别", "BMI", "子女数量", "是否吸烟", "区域"]]
    y = df["医疗费用"]
    
    # 6. 对分类特征进行独热编码（中文分类值）
    cat_features = ["性别", "是否吸烟", "区域"]  # 中文分类特征列名
    cat_encoder = OneHotEncoder(sparse_output=False, drop=None)
    encoded_cat_data = cat_encoder.fit_transform(X[cat_features])
    
    # 7. 构造编码后的中文特征名（与FEATURE_NAMES对齐）
    encoded_feature_names = []
    for i, feat in enumerate(cat_features):
        for cat in cat_encoder.categories_[i]:
            encoded_feature_names.append(f"{feat}_{cat}")
    
    # 8. 合并数值特征与编码后的分类特征
    numeric_features = X[["年龄", "BMI", "子女数量"]].reset_index(drop=True)
    encoded_features_df = pd.DataFrame(encoded_cat_data, columns=encoded_feature_names)
    X_processed = pd.concat([numeric_features, encoded_features_df], axis=1)
    
    # 9. 确保特征列顺序与预设FEATURE_NAMES完全一致
    # 补充缺失的特征列（防止编码后列名不匹配）
    for col in FEATURE_NAMES:
        if col not in X_processed.columns:
            X_processed[col] = 0
    X_processed = X_processed[FEATURE_NAMES]
    
    return X_processed, y, cat_encoder

def train_model():
    """训练模型并保存（仅当模型不存在时执行）"""
    if os.path.exists(MODEL_PATH):
        return  # 模型已存在，直接返回
    
    try:
        # 加载预处理后的数据
        X_processed, y, _ = load_and_preprocess_data()
        
        # 划分训练集与测试集（8:2分割）
        X_train, _, y_train, _ = train_test_split(
            X_processed, y, test_size=0.2, random_state=42
        )
        
        # 训练随机森林回归模型（参数适配医疗费用预测场景）
        rf_model = RandomForestRegressor(
            n_estimators=120,  # 树数量优化
            max_depth=10,      # 限制树深度避免过拟合
            random_state=42
        )
        rf_model.fit(X_train, y_train)
        
        # 保存训练好的模型
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(rf_model, f)
        
        st.success(f"✅ 模型训练完成！已保存至 {MODEL_PATH}")
    except Exception as e:
        st.error(f"❌ 模型训练失败：{str(e)}")
        st.stop()

# ===================== 页面功能函数（纯中文交互） =====================
def introduce_page():
    """应用简介页面（中文说明）"""
    st.write("欢迎使用医疗费用预测应用！")
    st.sidebar.success("点击「预测医疗费用」开始使用")
    st.markdown("""
    # 医疗费用预测应用 🩺
    基于真实医疗数据集（insurance-chinese.csv）训练，可根据投保人信息预测年度医疗费用，为保险定价提供参考。
    
    ## 数据集信息
    - 数据量：1338条投保人记录
    - 核心特征：年龄、性别、BMI、子女数量、吸烟状态、居住区域
    - 预测目标：年度医疗费用（单位：元）
    
    ## 使用指南
    1. 在「预测医疗费用」页面输入投保人信息；
    2. 点击「生成预测结果」按钮，获取费用预测值；
    3. 预测结果仅为参考，不具备法律效应。
    
    技术支持：support@example.com
    """)

def predict_page():
    """预测页面（纯中文交互，无英文映射）"""
    st.markdown("# 医疗费用预测")
    st.markdown("请输入投保人以下信息，系统将预测其年度医疗费用：")
    
    # 表单收集用户输入（纯中文，直接适配数据集）
    with st.form("insurance_pred_form"):
        # 1. 年龄（滑块输入）
        age = st.slider(
            "年龄", 
            min_value=18, max_value=100, value=30,
            help="投保人的实际年龄（建议18-100岁）"
        )
        
        # 2. 性别（中文选项，直接使用）
        sex = st.radio(
            "性别", 
            options=["女性", "男性"], 
            index=0,
            help="投保人的性别"
        )
        
        # 3. BMI（数值输入）
        bmi = st.number_input(
            "BMI（身体质量指数）", 
            min_value=10.0, max_value=50.0, value=22.5,
            help="BMI=体重(kg)/身高(m)²，正常范围18.5-23.9"
        )
        
        # 4. 子女数量（整数输入）
        children = st.number_input(
            "子女数量", 
            min_value=0, max_value=10, value=0, step=1,
            help="投保人需要抚养的子女数量"
        )
        
        # 5. 吸烟状态（中文选项，直接使用）
        smoker = st.radio(
            "是否吸烟", 
            options=["是", "否"], 
            index=1,
            help="投保人当前是否有吸烟习惯"
        )
        
        # 6. 居住区域（中文选项，直接使用）
        region = st.selectbox(
            "居住区域", 
            options=["东南部", "东北部", "西北部", "西南部"],
            index=0,
            help="投保人长期居住的区域"
        )
        
        # 提交按钮
        submit_btn = st.form_submit_button("生成预测结果", type="primary")
        
        # 提交后处理逻辑
        if submit_btn:
            # 1. 初始化特征向量（与中文FEATURE_NAMES顺序一致）
            feature_vector = [0] * len(FEATURE_NAMES)
            # 填充数值特征
            feature_vector[FEATURE_NAMES.index("年龄")] = age
            feature_vector[FEATURE_NAMES.index("BMI")] = bmi
            feature_vector[FEATURE_NAMES.index("子女数量")] = children
            # 填充分类特征（独热编码，中文值直接匹配）
            feature_vector[FEATURE_NAMES.index(f"性别_{sex}")] = 1
            feature_vector[FEATURE_NAMES.index(f"是否吸烟_{smoker}")] = 1
            feature_vector[FEATURE_NAMES.index(f"区域_{region}")] = 1
            
            # 2. 加载模型（无模型则自动训练）
            if not os.path.exists(MODEL_PATH):
                with st.spinner("首次使用，正在训练模型...（约10秒）"):
                    train_model()
            
            # 3. 加载模型并预测
            try:
                if not os.path.exists(MODEL_PATH):
                    st.error("❌ 模型训练失败，无法加载预测模型")
                    return
                
                with open(MODEL_PATH, "rb") as f:
                    rf_model = pickle.load(f)
                
                # 构造输入DataFrame（中文列名匹配）
                input_df = pd.DataFrame([feature_vector], columns=FEATURE_NAMES)
                # 预测医疗费用
                pred_charges = rf_model.predict(input_df)[0]
                
                # 4. 展示预测结果（中文格式化）
                st.success("### 预测结果")
                st.info(f"投保人年度医疗费用约为：**{round(pred_charges, 2)} 元**")
                # 补充参考信息（基于实际数据分布）
                if smoker == "是":
                    st.warning("⚠️ 提示：吸烟状态对医疗费用影响较大，建议优先考虑戒烟干预")
                if bmi > 28:
                    st.warning("⚠️ 提示：BMI偏高可能增加医疗支出，建议关注健康饮食与运动")
            
            except Exception as e:
                st.error(f"❌ 预测出错：{str(e)}")
                st.info("建议解决方案：\n1. 删除rf_insurance_model.pkl后重新运行（重新训练模型）\n2. 检查数据集文件是否完整")

# ===================== 主程序入口 =====================
def main():
    # 页面基础配置（中文标题+图标）
    st.set_page_config(
        page_title="医疗费用预测（中文数据集版）",
        page_icon="🩺",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # 侧边栏导航
    st.sidebar.title("功能导航")
    nav_choice = st.sidebar.radio(
        "请选择功能",
        ["应用简介", "预测医疗费用"],
        index=0
    )
    
    # 路由到对应页面
    if nav_choice == "应用简介":
        introduce_page()
    else:
        predict_page()

if __name__ == "__main__":
    main()
