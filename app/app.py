from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

from modules.exceptions import APIException


def touch_models():
    import db.models

    db.models  # Thanks pycharm for deleting my unused imports


def create_app() -> FastAPI:
    touch_models()
    from modules.auth.router import auth_router
    from modules.users.router import users_router
    from gql.app import graphql_app

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(users_router, prefix="/api/users", tags=["Users"])
    app.mount("/static", StaticFiles(directory="static"), name="static")

    app.mount("/graphql", graphql_app)

    @app.exception_handler(APIException)
    async def handle_api_exception(request, exc: APIException):
        return JSONResponse(
            {"code": exc.code, "detail": exc.detail},
            status_code=exc.status_code,
        )

    return app
