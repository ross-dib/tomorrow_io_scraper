"""
Data models weather data response from clients.io
using Pydantic models --> https://docs.pydantic.dev/latest/concepts/models/
"""
from pydantic import BaseModel


class TomorrowIOResponse(BaseModel):
    # TODO
    # name: str
    #color: Literal['red', 'green']
    #weight: Annotated[float, Gt(0)]
    #bazam: Dict[str, List[Tuple[int, bool, float]]]


