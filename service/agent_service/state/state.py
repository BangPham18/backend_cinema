from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import AnyMessage

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    classify: str
    email: str
    name: str
    birthday: str
    ten_phim: str
    ngay: str
    gio: str
    sex: str
    ghe: List[str]
    dang_nhap: str
