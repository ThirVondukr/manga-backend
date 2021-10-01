from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


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
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.mount("/static", StaticFiles(directory="static"), name="static")

    app.mount("/graphql", graphql_app)

    return app
