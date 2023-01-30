from pydantic import BaseModel

# -------------------------------------------------#
#                   500 - Server Error             #
# -------------------------------------------------#


class Error500(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            'example':
                {
                    'detail': 'Server Error',
                }
        }


error_server_open_api = {
    500: {
        "model": Error500,
        "description": "Servor Error"
    },
}


# -------------------------------------------------#
#                   204 - No Content               #
# -------------------------------------------------#


no_content_open_api = {
    204: {
        "description": "No Content"
    },
}
