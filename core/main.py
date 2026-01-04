import asyncio
import hashlib

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse, Response
from models import URL_MODEL, Base
from schemas import URL_SCHEMA
from sqlalchemy.future import select
from database import engine, SessionDep

app = FastAPI()



@app.post("/setup")
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    

async def hash_url(url) -> str:
    def compute_hash():
        full_hash = hashlib.sha256(url.encode('utf-8')).hexdigest()
        return full_hash[:5]
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, compute_hash)


@app.post("/posturl")
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

@app.get("/{short_hash}")
async def redirect(short_hash:str,
                   session: SessionDep):
    result = await session.execute(
        select(URL_MODEL).where(URL_MODEL.short_url==short_hash)
    )
    url_obj = result.scalar_one_or_none()
    if not url_obj:
        raise HTTPException(
            status_code=404
        )
    
    url_obj.clicks+=1

    return RedirectResponse(
        url=url_obj.long_url,
        status_code=307
        )
