from pydantic import BaseModel, Field, EmailStr, ValidationError, validator, root_validator
from typing import Optional
import datetime
import uuid


class Blog(BaseModel):
    # id: str = Field(title="The blog post ID - Auto generated",
    #                 default=uuid.uuid4())
    category: str = Field(
        title="Blog category name i.e. Python Development")

    sub_category: str = Field(
        title="Blog sub category i.e. From Scripting to Software")
    title: str = Field(
        title="Blog title i.e. The Import Module, Python's Import System In Software Development")

    description: str = Field(
        title="Blog short description")

    tags: list = Field(
        title="Blog post tags")

    image_url: str = Field(
        title="Blog title image - AWS Cloudfront")

    author: str = Field(
        title="Blog post author")

    creation_date: str = Field(
        default=datetime.datetime.now(), title="Date created", )

    content: list = Field(
        title="Blog post table of content")

    tldr: str = Field(
        title="Blog tldr")

    series_name: Optional[str] = Field(
        title="Blog series name, if part of a series")

    series_number: int = Field(
        title="Blog series number, if part of a series")

    featured_post: bool = Field(
        title="Is blog post a featured article?")

    def blog_post(self):
        return {
            "category": self.category,
            "sub_category": self.sub_category,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "image_url": self.image_url,
            "author": self.author,
            "creation_date": self.creation_date,
            "content": self.content,
            "tldr": self.tldr,
            "series_name": self.series_name,
            "series_number": self.series_number,
            "featured_post": self.featured_post
        }

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {


            }
        }


class Errors(BaseModel):
    loc: str
    msg: str
