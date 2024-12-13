import requests

def notify(message):
    # LINEチャネルアクセストークンを設定
    access_token = "5BOj6oXoPCtRR8/zI04uxp1oZjaOUuG0RiBf1HuS0n+e7ym9aj14p5YIcBE+RCSyeHmWseu/J2gQTVzGn/gwUuCeYJtSLK0v0X4RUxtyPxv7YjLT0IfdUin+gyL6UVK59Tp8JMSx8eRLs4EZ4oTu+AdB04t89/1O/w1cDnyilFU="  # LINE Developersから取得したアクセストークン

    url = "https://api.line.me/v2/bot/message/broadcast"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    payload = {
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("メッセージが送信されました")
        print("レスポンス:", response.json())
    else:
        print(f"エラー: {response.status_code}, {response.text}")



