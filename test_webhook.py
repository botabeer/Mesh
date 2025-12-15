"""
اختبار سرعة الـ webhook
يجب أن يكون الرد أقل من 500ms
"""
import time
import requests
import json
import hmac
import hashlib
import base64

def test_webhook_speed(url, channel_secret):
    """اختبار سرعة استجابة الـ webhook"""
    
    # تجهيز البيانات
    test_data = {
        "events": [{
            "type": "message",
            "message": {
                "type": "text",
                "text": "test"
            },
            "source": {
                "userId": "test_user_123"
            },
            "replyToken": "test_token"
        }]
    }
    
    body = json.dumps(test_data)
    
    # حساب التوقيع
    signature = base64.b64encode(
        hmac.new(
            channel_secret.encode('utf-8'),
            body.encode('utf-8'),
            hashlib.sha256
        ).digest()
    ).decode('utf-8')
    
    headers = {
        'Content-Type': 'application/json',
        'X-Line-Signature': signature
    }
    
    # قياس الوقت
    times = []
    for i in range(10):
        start = time.time()
        try:
            response = requests.post(
                url,
                data=body,
                headers=headers,
                timeout=5
            )
            elapsed = (time.time() - start) * 1000  # ms
            times.append(elapsed)
            
            print(f"Test {i+1}: {elapsed:.2f}ms - Status: {response.status_code}")
            
        except requests.exceptions.Timeout:
            print(f"Test {i+1}: TIMEOUT")
            times.append(5000)
        except Exception as e:
            print(f"Test {i+1}: ERROR - {e}")
            times.append(5000)
        
        time.sleep(0.5)
    
    # النتائج
    avg = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print("\n" + "="*50)
    print("نتائج الاختبار:")
    print(f"متوسط الوقت: {avg:.2f}ms")
    print(f"أسرع وقت: {min_time:.2f}ms")
    print(f"أبطأ وقت: {max_time:.2f}ms")
    print("="*50)
    
    if avg < 500:
        print("✓ ممتاز - الرد سريع جداً")
    elif avg < 1000:
        print("✓ جيد - الرد مقبول")
    else:
        print("✗ بطيء - يحتاج تحسين")
    
    return avg

def test_health_endpoint(url):
    """اختبار endpoint الصحة"""
    try:
        start = time.time()
        response = requests.get(f"{url}/health", timeout=5)
        elapsed = (time.time() - start) * 1000
        
        print(f"\nHealth Check: {elapsed:.2f}ms - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Queue Size: {data.get('queue_size', 'N/A')}")
            print(f"Active Games: {data.get('active_games', 'N/A')}")
        return True
    except Exception as e:
        print(f"Health Check Error: {e}")
        return False

if __name__ == "__main__":
    # ضع رابط السيرفر هنا
    SERVER_URL = "https://your-server.onrender.com/callback"
    CHANNEL_SECRET = "your_channel_secret"
    
    print("بدء اختبار السرعة...")
    print(f"Server: {SERVER_URL}\n")
    
    # اختبار الصحة أولاً
    test_health_endpoint(SERVER_URL.replace('/callback', ''))
    
    # اختبار الـ webhook
    avg_time = test_webhook_speed(SERVER_URL, CHANNEL_SECRET)
