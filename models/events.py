from beanie import Document
from pydantic import BaseModel
from typing import List, Optional

class Event(BaseModel):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
    
    #이벤트의 샘플 데이터를 정의 - API를 통해 신규 이벤트를 생성할 때 참고
    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI Book Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the contents of the Fast API book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }
    class Settings:
        name = "events"
        
class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[str]
    location: Optional[str]
    
    class Config:
        schema_extra = {
            "example": {
                "title": "Fast API BOOK Launch",
                "image": "https://linktomyimage.com/image.png",
                "description": "We will be discussing the cotents of the FastAPI book in this event. Ensure to come with your own copy to win gifts!",
                "tags": ["python", "fastapi", "book", "launch"],
                "location": "Google Meet"
            }
        }