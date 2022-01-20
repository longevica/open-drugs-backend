from os import getenv
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

from endpoints import experiment
from config import CONFIG, VERSION
from db.dao import BaseDAO


def assembling_endpoints(app: FastAPI):
    app.include_router(
        experiment.router,
        tags=["experiment"],
    )


origins = [
    "*",
]


def init():
    app = FastAPI(
        debug=CONFIG.get('DEBUG'),
        title='LISTControls backend CMS',
        root_path=getenv('ROOT_PATH')
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    assembling_endpoints(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = init()


class Version(BaseModel):
    major: str
    minor: str
    build: Optional[str]
    date: Optional[str]
    revision: Optional[str]
    branch: Optional[str]


@app.get("/version")
def version() -> dict:
    """
    Version information for the running application instance
    """
    return VERSION


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=str(VERSION.get('major')) + '.' + str(VERSION.get('minor')) + '.' + str(VERSION.get('build')),
        routes=app.routes,
        servers=[{'url': str(CONFIG.get('API_HOST')) + ':' + str(CONFIG.get('API_PORT'))}],
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == "__main__":
    # db conn init
    _ = BaseDAO()
    # run
    uvicorn.run(
        "main:app",
        host=CONFIG['CMS_HOST'],
        port=int(CONFIG['CMS_PORT']),
        reload=CONFIG.get('RELOAD'),
        debug=CONFIG.get('DEBUG'),  # debug=True implies reload=True
    )
