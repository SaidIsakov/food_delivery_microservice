import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from app.consumer import consume_events
from app.database import events_collection, mongodb_client


@asynccontextmanager
async def lifespan(app: FastAPI):
  task = asyncio.create_task(consume_events(events_collection))
  try:
    yield
  finally:
    task.cancel()

    with suppress(asyncio.CancelledError):
      await task

    await mongodb_client.close()

app = FastAPI(lifespan=lifespan)



@app.get('/events')
async def get_events(limit: int = 5):
  quary = events_collection.find().sort("created_at", -1).limit(limit)
  return await quary.to_list(limit)
