# Data models used in the onboarding
# NOTE: This file should not be modified
from datetime import datetime
from pydantic import model_validator
from sqlmodel import Field

from backend.data.base_model import BaseSQLModel
from backend.data.enums import CommandStatus


class MainCommand(BaseSQLModel, table=True):
    """
    Main command model.
    This table represents all the possible commands that can be issued.

    List of commands: https://docs.google.com/spreadsheets/d/1XWXgp3--NHZ4XlxOyBYPS-M_LOU_ai-I6TcvotKhR1s/edit?gid=564815068#gid=564815068
    """

    id: int | None = Field(
        default=None, primary_key=True
    )  # NOTE: Must be None for autoincrement
    name: str
    params: str | None = None
    format: str | None = None
    data_size: int
    total_size: int

    @model_validator(mode="after")
    def validate_params_format(self):
        if self.params is None or self.format is None:
            if type(self.params) is not type(self.format):
                raise ValueError
        else:
            if self.params and self.format is not None:
                foo = self.params.split(',')
                bar = self.format.split(',')
                if len(foo) == len(bar):
                    return self
                else:
                    raise ValueError


class Command(BaseSQLModel, table=True):
    """
    An instance of a MainCommand.
    This table holds the data related to actual commands sent from the ground station up to the OBC.
    """

    id: int | None = Field(
        default=None, primary_key=True
    )  # NOTE: Must be None for autoincrement
    command_type: int = Field(
        foreign_key="maincommand.id"
    )  # Forign key must be a string
    status: CommandStatus = CommandStatus.PENDING
    params: str | None = None
    created_on: datetime = datetime.now()
    updated_on: datetime = datetime.now()
