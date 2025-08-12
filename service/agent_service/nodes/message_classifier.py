from pydantic import BaseModel, Field
from typing import Literal


class MessageClassifier(BaseModel):
    message_type: Literal["tư vấn", "đặt vé"] = Field(
        ...,
        description="""Phân loại tin nhắn người dùng thành "tư vấn" hoặc "đặt vé" """
    )
