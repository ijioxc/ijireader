import os
import json
import asyncio
import sys

# 檢查是否安裝了 edge-tts
try:
    import edge_tts
except ImportError:
    print("請先安裝 edge-tts: pip install edge-tts")
    sys.exit(1)

async def generate_for_chapter(text, output_file):
    # 使用微軟的英文優質女聲 en-US-AriaNeural
    # 你也可以換成 en-US-GuyNeural (男聲)
    voice = "en-US-AriaNeural"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    print(f"Generated: {output_file}")

async def main():
    base_dir = "/Users/ijioxc/Desktop/英文code/ijieng/books"
    chapters_dir = os.path.join(base_dir, "gatsby_chapters")
    
    for i in range(1, 10):
        chap_folder = os.path.join(chapters_dir, f"chapter-{i}")
        json_path = os.path.join(chap_folder, "content.json")
        
        if not os.path.exists(json_path):
            print(f"File not found: {json_path}")
            continue
            
        print(f"Processing Chapter {i} with Edge TTS...")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            lines = data.get("content", [])
            
        full_text = "\n".join(lines)
        output_mp3 = os.path.join(chap_folder, f"chapter-{i}_edge.mp3")
        
        await generate_for_chapter(full_text, output_mp3)

if __name__ == "__main__":
    # 在有些系統上可能需要這個
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
