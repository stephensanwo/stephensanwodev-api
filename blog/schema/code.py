from pydantic import BaseModel, Field, EmailStr, ValidationError, validator, root_validator
from typing import Optional, List
from bson import ObjectId
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Code(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    code_id: str = Field(...,
                         title="Code post id -> Sequential post ID for code post")

    category: str = Field(...,
                          title="Code category id -> this post will be added to the specified category ID")

    title: str = Field(...,
                       title="Code title i.e. The Import Module, Python's Import System In Software Development")

    description: str = Field(...,
                             title="Code short description")

    tags: list = Field(...,
                       title="Code post tags")

    code_url: str = Field(
        title="URL extension of the code post"
    )

    author: str = Field(...,
                        title="Code post author")

    creation_date: datetime = Field(
        default=datetime.now(), title="Date created")

    def code_post(self):
        return {
            "category": self.category,
            "code_id": self.code_id,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "author": self.author,
            "code_url": self.code_url,
            "creation_date": self.creation_date,
        }

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {

            }
        }


class Errors(BaseModel):
    loc: str
    msg: str


class CodeList(BaseModel):
    code_posts: List[Code]
