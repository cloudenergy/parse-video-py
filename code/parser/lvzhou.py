import re

import httpx
from bs4 import BeautifulSoup

from .base import BaseParser, VideoAuthor, VideoInfo


class LvZhou(BaseParser):
    """
    绿洲
    """

    async def parse_share_url(self, share_url: str) -> VideoInfo:
        async with httpx.AsyncClient() as client:
            response = await client.get(share_url, headers=self.get_default_headers())
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        video_element = soup.select_one("video")
        video_url = video_element.get('src') if video_element else None
        
        avatar_img = soup.select_one("a.avatar img")
        author_avatar = avatar_img.get('src') if avatar_img else None
        
        video_cover = soup.select_one("div.video-cover")
        video_cover_style = video_cover.get('style', '') if video_cover else ''

        cover_url = ""
        if video_cover_style:
            match = re.search(r"background-image:url\((.*)\)", video_cover_style)
            if match:
                cover_url = match.group(1)

        title_element = soup.select_one("div.status-title")
        title = title_element.text if title_element else None
        
        author_name_element = soup.select_one("div.nickname")
        author_name = author_name_element.text if author_name_element else None

        return VideoInfo(
            video_url=video_url,
            cover_url=cover_url,
            title=title,
            author=VideoAuthor(
                name=author_name,
                avatar=author_avatar,
            ),
        )

    async def parse_video_id(self, video_id: str) -> VideoInfo:
        share_url = f"https://m.oasis.weibo.cn/v1/h5/share?sid={video_id}"
        return await self.parse_share_url(share_url)
