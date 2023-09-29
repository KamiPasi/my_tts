from fastapi import FastAPI, Request, responses
import edge_tts

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/tts")
async def read_item(request: Request):
    body = await request.json()
    media_type = 'audio/mpeg'
    params = body
    text = params['text'].strip()
    if 'rate' in params.keys():
        # print(params['rate'], type(params['rate']))
        rate = int(params['rate'])
        rate = f'+{rate * 2}%'
        communicate = edge_tts.Communicate(text, 'zh-CN-YunjianNeural', rate=rate)
    else:
        communicate = edge_tts.Communicate(text, 'zh-CN-YunjianNeural')

    return responses.StreamingResponse(
        content=tts_stream2(communicate),
        media_type=media_type
    )


async def tts_stream2(communicate):
    async for message in communicate.stream():
        if message['type'] == "audio":
            yield message['data']



# uvicorn mytts:app --host 0.0.0.0 --port 8999 --reload
