
import qrcode

from fastapi import APIRouter, Response, Depends, HTTPException, status, File, UploadFile

from ..users.models import User
from ..authentication.encryption import get_current_user

from .document_recognizer import document_analysis_client

router = APIRouter(
    prefix="/api/v1/users/{user_id}/utility"
)


@router.get(path="getQrCode/{string_to_encode:path}/",
            tags=['utility'])
async def get_form_qr_code(
        user_id: str,
        string_to_encode: str,
        current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID from path doesnt match your user id.")

    # Converts the link in a qr code and saves the image
    img = qrcode.make(string_to_encode)
    img.save("./api/utility/qr_code.png")

    # Opens the image in byte format, since that's what we can send
    with open("./api/utility/qr_code.png", "rb") as file:
        return Response(content=file.read(), media_type="image/png")


# This endpoint function is not declared as async so it runs in another thread
@router.post(path="scan_document/",
            tags=['utility'])
async def scan_document(
        user_id: str,
        document: UploadFile = File(),
        current_user: User = Depends(get_current_user),
):

    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User ID from path doesnt match your user id.")

    document_content = await document.read()

    poller = document_analysis_client.begin_analyze_document(
            "prebuilt-document", document=document_content
        )

    result = poller.result()

    api_result = {}

    for kv_pair in result.key_value_pairs:
        key = kv_pair.key
        value = kv_pair.value

        if key and value and key.content and value.content:
            if '/' in key.content:
                key_splits = key.content.split('/')
            else:
                key_splits = key.content.split()

            if 'Loc nastere' in key.content:
                clean_key = 'loc nastere'
            else:
                clean_key = key_splits[0]

            api_result[clean_key] = value.content

    return api_result
