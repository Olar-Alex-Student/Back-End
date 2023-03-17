
import qrcode

from fastapi import APIRouter, Response, Depends, HTTPException, status

from ..users.models import User
from ..authentication.encryption import get_current_user

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
