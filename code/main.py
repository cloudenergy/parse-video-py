import re
from parser import VideoSource, parse_video_id, parse_video_share_url

import uvicorn
from fastapi import FastAPI, Request
import json


app = FastAPI()


@app.get("/video/share/url/parse")
async def share_url_parse(url: str):
    url_reg = re.compile(r"http[s]?:\/\/[\w.-]+[\w\/-]*[\w.-]*\??[\w=&:\-\+\%]*[/]*")
    video_share_url = url_reg.search(url).group()

    try:
        video_info = await parse_video_share_url(video_share_url)
        return {"code": 200, "msg": "解析成功", "data": video_info.__dict__}
    except Exception as err:
        return {
            "code": 500,
            "msg": str(err),
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
