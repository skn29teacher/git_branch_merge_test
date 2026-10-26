"""팀원 A: 작업 생성 API.

실행: python amugona.py
실습 화면: http://127.0.0.1:8000/docs
데이터는 메모리에 저장되며 서버를 다시 실행하면 초기화됩니다.
"""

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="팀 할 일 관리 API")
router = APIRouter(prefix="/tasks", tags=["작업 생성"])

# 팀 기능을 통합할 때는 이 리스트를 공통 storage.py로 옮겨 함께 사용하세요.
tasks: list[dict] = []


class TaskCreate(BaseModel):
    # id는 서버가 만들기 때문에 요청 본문에는 넣지 않습니다.
    name: str = Field(min_length=1)
    message: str = Field(min_length=1)
    assignee: str = Field(min_length=1)
    done: bool = False


@router.post("", status_code=201)
def create_task(payload: TaskCreate):
    # 목록이 비어 있어도 1부터 시작하며, 현재 목록의 ID와 겹치지 않습니다.
    task_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": task_id, **payload.model_dump()}
    tasks.append(task)
    return task


app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
