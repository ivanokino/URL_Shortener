import hashlib
import asyncio

from fastapi import HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from sqlalchemy.future import select

from models import URL_MODEL
from schemas import URL_SCHEMA
from database import SessionDep

#################
async def hash_url(url) -> str:
    def compute_hash():
        full_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
        return full_hash[:5]
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, compute_hash)
##################

router = APIRouter()

@router.post("/posturl")
async def post_url(url:URL_SCHEMA, session:SessionDep):
    ######
    result = await session.execute(
        select(URL_MODEL).where(URL_MODEL.long_url == url.long_url)
    )
    url_obj = result.scalar_one_or_none()
    if url_obj:
        return {"url":url_obj.short_url }
    ######

    new_url = URL_MODEL()
    new_url.long_url = url.long_url
    
    
    new_url.short_url = await hash_url(url.long_url)  
    session.add(new_url)
    await session.commit()

    return{"url":new_url.short_url}

@router.get("/{short_hash}")
async def redirect(short_hash:str,
                   session: SessionDep):
    result = await session.execute(
        select(URL_MODEL).where(URL_MODEL.short_url==short_hash)
    )
    url_obj = result.scalar_one_or_none()
    if not url_obj:
        raise HTTPException(
            status_code=404,
            detail="Cant find URL"
        )
    
    url_obj.clicks+=1

    return RedirectResponse(
        url=url_obj.long_url,
        status_code=307
        )