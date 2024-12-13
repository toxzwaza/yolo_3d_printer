import requests
import subprocess
import os

# MJPG-streamerのスナップショットURL
snapshot_url = "http://192.168.210.91:8080/?action=snapshot"

# スナップショット画像の保存先
snapshot_path = "snapshot.jpg"

# YOLO detect.py スクリプトのパス
detect_script_path = "detect.py"

# YOLO結果の保存ディレクトリ
output_dir = "runs/detect"

def get_snapshot(url, save_path):
    """
    スナップショット画像を取得して保存
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # HTTPエラーを検出
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Snapshot saved to {save_path}")
    except Exception as e:
        print(f"Failed to get snapshot: {e}")
        return False
    return True

def analyze_snapshot(image_path):
    """
    detect.py を使用してスナップショットを解析
    """
    try:
        # サブプロセスで detect.py を呼び出す
        result = subprocess.run(
            [
                "python", detect_script_path,
                "--weights", "runs/train/exp9/weights/best.pt",  # 学習済みモデル
                "--conf", "0.5",            # 信頼度しきい値
                "--source", image_path,     # スナップショット画像
                "--project", output_dir,    # 結果保存先
                "--name", "snapshot_result" # 結果フォルダ名
            ],
            capture_output=True,
            text=True
        )
        # detect.py の出力を表示
        print(result.stdout)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Failed to analyze snapshot: {e}")
        return False
    return True

import time

if __name__ == "__main__":
    while True:
        # スナップショットを取得
        if get_snapshot(snapshot_url, snapshot_path):
            # YOLOで解析
            if analyze_snapshot(snapshot_path):
                print("Snapshot analyzed successfully.")
            else:
                print("Failed to analyze snapshot.")
        else:
            print("Failed to get snapshot.")
        
        # 5分間隔で実行
        time.sleep(300)
