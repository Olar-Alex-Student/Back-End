from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

from api.users import user_router
from api.forms import form_router
from api.form_submissions import submission_router

from api.authentication import oath2

description = """
The Bizonii backend API. 🐂

## Users

* You can **GET** all of **your** data.
* You can **POST** to create **new users**.
* You can **PUT** to update **your** data.
* You can **DELETE** **your** account.

## Forms

* _NOT IMPLEMENTED_
"""

app = FastAPI(
    title="Bizonii Backend",
    description=description,
    version="0.0.0",
    license_info={
        "name": "CC0",
        "url": "https://creativecommons.org/publicdomain/zero/1.0/"},
    contact={
        "name": "Vizitiu Valentin",
        "email": "vizitiuvalentin12@gmail.com"}
)

app.include_router(user_router.router)
app.include_router(form_router.router)
app.include_router(submission_router.router)
app.include_router(oath2.router)


@app.get("/", include_in_schema=False)
async def send_to_docs() -> RedirectResponse:
    # Since the url for the backend is different from the frontend, if the user accesses the base url, redirect them
    # to the docs page directly

    return RedirectResponse(url="./docs")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
