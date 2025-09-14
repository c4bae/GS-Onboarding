from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.api.models.request_model import CommandRequest
from backend.api.models.response_model import CommandListResponse, CommandSingleResponse
from backend.data.data_models import Command
from backend.data.engine import get_db

# Prefix: "/commands"
command_router = APIRouter(tags=["Commands"])


@command_router.get("/", response_model=CommandListResponse)
def get_commands(db: Session = Depends(get_db)):
    """
    Gets all the items

    :return: Returns a list of commands
    """
    query = select(Command)
    items = db.exec(query).all()
    return {"data": items}


@command_router.post("/", response_model=CommandSingleResponse)
def create_command(payload: CommandRequest, db: Session = Depends(get_db)):
    command = Command(command_type=payload.command_type, params=payload.params)
    db.add(command)
    db.commit()

    added_payload = select(Command).order_by(Command.id.desc())
    result = db.exec(added_payload).first()

    return {"data": result}

@command_router.delete("/{id}", response_model=CommandListResponse) # if a response_model is provided you must return it in the right format or compiler gets angry
def delete_command(id: int, db: Session = Depends(get_db)):
    command_to_delete = select(Command).where(Command.id == id)
    results = db.exec(command_to_delete)
    command = results.first()
    if command:
        db.delete(command)
        db.commit()

        results = db.exec(select(Command))
        commands = results.all()
        return CommandListResponse(data=commands)
    else:
        raise HTTPException(status_code=404)
