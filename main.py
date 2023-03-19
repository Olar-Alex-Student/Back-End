import asyncio

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

from api.users import user_router
from api.forms import form_router
from api.form_submissions import submission_router
from api.utility import utility_router

from background_tasks.delete_old_submissions import delete_expired_form_submissions


from api.authentication import oath2

description = """
The Bizonii backend API. 🐂

## Users

* You can **GET** all of **your** data.
* You can **POST** to create **new users**.
* You can **POST** to log in and get a token.
* You can **PUT** to update **your** data.
* You can **DELETE** **your** account.

## Forms

* You can **GET** a list of all forms with the title, id and expiration date.
* You can **POST** to create a new form.
* You can **GET** all the info about one form.
* You can **PUT** to update a form.
* You can **DELETE** a form.

## Submissions

* You can **GET** a list of all form submissions.
* You can **POST** to create a new form submission.
* You can **GET** all the info about one form submission.
* You can **PUT** to update a form submission if you are the owner of the form or the one who created the submission.
* You can **DELETE** a form submission.
* You can **DELETE** all form submissions for a given form.
* You can **GET** a pdf with the completed submission.

## Utility

* You can **GET** a QR Code from a string, for example to get a QR Code to the page where you can fill a submission.

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
app.include_router(utility_router.router)
app.include_router(oath2.router)


# Adds a background task to run every day to delete old submissions
@app.on_event("startup")
async def schedule_periodic():
    loop = asyncio.get_event_loop()
    loop.create_task(delete_expired_form_submissions())


@app.get("/", include_in_schema=False)
async def send_to_docs() -> RedirectResponse:
    # Since the url for the backend is different from the frontend, if the user accesses the base url, redirect them
    # to the docs page directly

    return RedirectResponse(url="./docs")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
