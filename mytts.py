from fastapi import FastAPI, Request, responses
import edge_tts

app = FastAPI()


@app.post("/")
async def read_item(request: Request):
    headers = request.headers
    body = await request.json()
    # print("headers:", headers)
    # print("body:", body)
    media_type = 'audio/mpeg'
    params = body
    text = params['text'].strip()
    print(text)

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



# uvicorn mytts2:app --host 0.0.0.0 --port 8999 --reload
