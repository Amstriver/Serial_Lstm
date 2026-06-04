import torch
import pandas as pd
import numpy as np
from model import TabNet
from sklearn.preprocessing import StandardScaler

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MODEL_PATH = "best_model.pth"

def predict_gas(csv_path):
    # 加载模型
    model = TabNet(input_size=3, num_classes=3).to(DEVICE)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE, weights_only=True))
    model.eval()

    # 读取数据
    df = pd.read_csv(csv_path)
    
    # 你训练用的3个传感器
    use_cols = ["sensor3", "sensor5", "sensor6"]
    X = df[use_cols].dropna().values

    # 标准化
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    X_tensor = torch.FloatTensor(X).to(DEVICE)

    # 预测
    with torch.no_grad():
        outputs = model(X_tensor)
        predictions = outputs.argmax(1).cpu().numpy()

    # 统计数量
    count0 = np.sum(predictions == 0)
    count1 = np.sum(predictions == 1)
    count2 = np.sum(predictions == 2)

    # 找出最多的一类
    max_count = max(count0, count1, count2)
    if max_count == count0:
        result = "C₂H₆O"
        result_code = 0
    elif max_count == count1:
        result = "NO"
        result_code = 1
    else:
        result = "NO₂"
        result_code = 2

    # 保存结果
    # df = df.dropna()
    # df['预测标签'] = predictions
    # df.to_csv("预测结果.csv", index=False, encoding='utf-8-sig')

    return {
        "result": result,
        "code": result_code,
        "乙醇": int(count0),
        "一氧化氮": int(count1),
        "二氧化氮": int(count2)
    }