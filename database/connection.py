# 데이터베이스 클라이언트 설정
from beanie import init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional, Any, List
from pydantic import BaseSettings, BaseModel
from models.users import User
from models.events import Event

class Setting(BaseSettings):
    DATABASE_URL: Optional[str] = None
    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
            document_models=[Event, User])
    
    class Config:
        env_file = ".env"
            
#데이터베이스 초기화중에 사용되는 모델은 Event, User 문서의 모델이다.
class Database:
    def __init__(self, model):
        self.model = model
    
    #document의 인스턴스를 받아서 데이터베이스 인스턴스에 전달합니다.    
    async def save(self, document) -> None:
        await document.create()
        return
    
    #데이터베이스 컬렉션에서 단일 레코드를 불러올 떄 사용하는 메서드
    #ID를 인수로 받아 컬렉션에서 일치하는 레코드를 불러온다.
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id)
        if doc:
            return doc
        return False
    
    #데이터베이스 컬렉션에서 전체 레코드를 불러올 때 사용하는 메서드
    #인수가 없다
    async def get_all(self) -> List[Any]:
        docs = await self.model.find_all().to_list()
        return docs    
    
    #update 메서드, Any: 어떤 형태의 메소드도 반환할 수 있다
    #update() 메서드는 하나의 ID와 pydantic 스키마를 인수로 받는다. 스키마에는 클라이언트가 보낸 PUT 요청에 의해 변경된 필드가 저장된다.
    #변경된 요청 바디는 딕셔너리에 저장된 다음 None 값을 제외하도록 필터링된다. 이 작업이 완료되면 변경 쿼리에 저장되고 beanie의 update()메서드를 통해 실행된다.
    async def update(self, id: PydanticObjectId, body: BaseModel) -> Any:
        doc_id = id
        des_body = body.dic()
        des_body = {k:v for k,v in des_body.items() if v is not None}
        update_query = {"$set": {
            field: value for field, value in des_body.items()
        }}
        
        doc = await self.get(doc_id)
        if not doc:
            return False
        await doc.update(update_query)
        return doc
    
    #해당 레코드가 있는지 확인하고 있으면 삭제합니다.
    async def delete(self, id:PydanticObjectId) -> bool:
        doc = await self.get(id)
        if not doc:
            return False
        await doc.delete()
        return True