import asyncio, edge_tts, os, nest_asyncio

nest_asyncio.apply()
os.makedirs("assets/audio", exist_ok=True)

async def gen():
    await edge_tts.Communicate("Tunde went to the local market with his mother.", "en-NG-AbeoNeural").save("assets/audio/english_passage.mp3")
    await edge_tts.Communicate("Afrobeats is a music genre that has taken the world by storm.", "en-NG-AbeoNeural").save("assets/audio/teen_passage.mp3")
    print("✅ Both MP3s generated in assets/audio/")

if __name__ == "__main__":
    asyncio.run(gen())