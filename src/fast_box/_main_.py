import uvicorn

from src.fast_box.settings import settings


uvicorn.run(
    'fast_box.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)
