from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from blog.database import Base
from blog.schemas import ORMBaseModel


def check_if_object_exists(query_result):
    if not query_result.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Object not found"
        )


def get_all(model: Base, db: Session):
    return db.query(model).all()


def get_details_by_id(model: Base, obj_id: int, db: Session):
    query_result = db.query(model).filter(model.id == obj_id)
    check_if_object_exists(query_result)

    return query_result.first()


def update_object_by_id(
    model: Base, obj_id: int, request_data: ORMBaseModel, db: Session
):
    query_result = db.query(model).filter(model.id == obj_id)
    check_if_object_exists(query_result)
    query_result.update(request_data.to_dict())
    db.commit()

    return {"result": f"Updated."}


def delete_object_by_id(model: Base, obj_id: int, db: Session):
    query_result = db.query(model).filter(model.id == obj_id)
    check_if_object_exists(query_result)
    query_result.delete()
    db.commit()

    return {"result": f"Deleted."}
