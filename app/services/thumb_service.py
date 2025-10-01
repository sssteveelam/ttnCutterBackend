import httpx
from bs4 import BeautifulSoup
from fastapi import HTTPException, status
import requests


async def get_facebook_thumbnail(url: str) -> str:
    try:
        async with httpx.AsyncClient(headers={"User-Agent": "Mozilla/ 5.0"}) as client:
            finaly_url = requests.get(url)
            print("finaly_Url : ---> ", str(finaly_url.url))
            response = await client.get(str(finaly_url.url))
            # Xu ly trang thai 200, 404, 500,...
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            og_image = soup.find("meta", property="og:image")

            if og_image and og_image.get("content"):
                return og_image["content"]

            raise ValueError("Thumbnail not found in Facebook page")

    except Exception as e:
        raise RuntimeError(f"Failed to extract Facebook thumbnail: {e}")


async def get_titkok_thumbnail(url: str) -> str:
    finaly_url = requests.get(url)
    oembed_url = f"https://www.tiktok.com/oembed?url={str(finaly_url.url)}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(oembed_url)

            response.raise_for_status()

            data = response.json()
            thumbnail_url = data.get("thumbnail_url")

            if not thumbnail_url:
                raise HTTPException(
                    status_code=404, detail="Thumbnail not found in TikTok response"
                )

            return {"thumbnailUrl": thumbnail_url}

    except httpx.HTTPStatusError as exc:
        return HTTPException(
            status_code=exc.response.status_code,
            detail=f"Failed to fetch from TikTok: {exc.response.text}",
        )
    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,  # Service Unavailable
            detail=f"An error occurred while requesting {exc.request.url!r}.",
        )
    except Exception:
        raise HTTPException(status_code=500, detail="An internal server error occurred")
