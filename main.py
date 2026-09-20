import os
import asyncio
import aiohttp
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent

TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME", "username_here")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "webhook_here")

client = TikTokLiveClient(unique_id=TIKTOK_USERNAME)

async def send_discord_notification(username):
    payload = {
        "content": f"🔴 **{username}** بدأ بث مباشر الآن على تيك توك!\nhttps://www.tiktok.com/@{username}/live",
        "username": "TikTok Live Notifier",
        "avatar_url": "https://sf-tb-sg.ibytedtos.com/obj/eden-sg/u3iwb3pq/tiktok_icon.png"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(DISCORD_WEBHOOK_URL, json=payload) as response:
                if response.status in (200, 204):
                    print("✅ تم إرسال الإشعار إلى ديسكورد بنجاح!")
                else:
                    print(f"❌ فشل إرسال الإشعار: {response.status}")
        except Exception as e:
            print(f"❌ حدث خطأ أثناء إرسال الإشعار: {e}")

@client.on(ConnectEvent)
async def on_connect(event: ConnectEvent):
    print(f"🎉 الحساب {TIKTOK_USERNAME} أونلاين وفي بث مباشر الآن!")
    await send_discord_notification(TIKTOK_USERNAME)

async def monitor_stream():
    print(f"👀 جاري مراقبة حساب @{TIKTOK_USERNAME}...")
    while True:
        try:
            if not client.is_connected:
                await client.start()
        except Exception:
            pass
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(monitor_stream())
