from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import edge_tts

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

@app.get("/tts")
async def tts(
    text: str,
    voice: str = Query(default="en-US-AndrewMultilingualNeural"),
    rate: str = Query(default="+0%"),
):
    communicate = edge_tts.Communicate(text, voice, rate=rate)

    async def stream_audio():
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

    return StreamingResponse(stream_audio(), media_type="audio/mpeg")
