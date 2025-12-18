import sys

print("Testing imports for line-bot-sdk v3...")

try:
    from linebot.v3 import WebhookHandler
    print("✓ WebhookHandler imported")
except ImportError as e:
    print(f"✗ WebhookHandler import failed: {e}")
    sys.exit(1)

try:
    from linebot.v3.exceptions import InvalidSignatureError
    print("✓ InvalidSignatureError imported")
except ImportError as e:
    print(f"✗ InvalidSignatureError import failed: {e}")
    sys.exit(1)

try:
    from linebot.v3.messaging import (
        Configuration,
        ApiClient,
        MessagingApi,
        ReplyMessageRequest,
        TextMessage
    )
    print("✓ Messaging classes imported")
except ImportError as e:
    print(f"✗ Messaging classes import failed: {e}")
    sys.exit(1)

try:
    from linebot.v3.webhooks import MessageEvent, TextMessageContent
    print("✓ MessageEvent and TextMessageContent imported")
except ImportError as e:
    print(f"✗ Webhook classes import failed: {e}")
    sys.exit(1)

try:
    from config import Config
    print("✓ Config imported")
except ImportError as e:
    print(f"✗ Config import failed: {e}")
    sys.exit(1)

try:
    from database import Database
    print("✓ Database imported")
except ImportError as e:
    print(f"✗ Database import failed: {e}")
    sys.exit(1)

try:
    from game_manager import GameManager
    print("✓ GameManager imported")
except ImportError as e:
    print(f"✗ GameManager import failed: {e}")
    sys.exit(1)

try:
    from text_manager import TextManager
    print("✓ TextManager imported")
except ImportError as e:
    print(f"✗ TextManager import failed: {e}")
    sys.exit(1)

try:
    from ui import UI
    print("✓ UI imported")
except ImportError as e:
    print(f"✗ UI import failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("All imports successful!")
print("="*50)

print("\nTesting app.py import...")
try:
    import app
    print("✓ app.py imported successfully")
    print(f"✓ Flask app object exists: {hasattr(app, 'app')}")
    print(f"✓ Handler object exists: {hasattr(app, 'handler')}")
    print(f"✓ Database object exists: {hasattr(app, 'db')}")
except Exception as e:
    print(f"✗ app.py import failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("SUCCESS: All tests passed!")
print("="*50)
