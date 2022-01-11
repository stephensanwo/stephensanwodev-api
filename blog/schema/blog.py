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


class Blog(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    post_id: str = Field(...,
                         title="Blog post id -> Sequential post ID for blog post")
    category: str = Field(...,
                          title="Blog category id -> this post will be added to the specified category ID")

    sub_category: str = Field(...,
                              title="Blog sub category string, this can vary i.e. From Scripting to Software")

    title: str = Field(...,
                       title="Blog title i.e. The Import Module, Python's Import System In Software Development")

    description: str = Field(...,
                             title="Blog short description")

    tags: list = Field(...,
                       title="Blog post tags")

    image_url: str = Field(...,
                           title="Blog title image - AWS Cloudfront")

    author: str = Field(...,
                        title="Blog post author")

    creation_date: datetime = Field(
        default=datetime.now(), title="Date created")

    content: list = Field(...,
                          title="Blog post table of content")

    tldr: str = Field(...,
                      title="Blog tldr")

    series_title: str = Field(
        title="Title for series, if part of a series")

    post_url: str = Field(
        title="URL extension of the blog post"
    )

    featured_post: bool = Field(...,
                                title="Is blog post a featured article? -> This will add the article to featured article")

    def blog_post(self):
        return {
            "category": self.category,
            "post_id": self.post_id,
            "sub_category": self.sub_category,
            "title": self.title,
            "description": self.description,
            "tags": self.tags,
            "image_url": self.image_url,
            "author": self.author,
            "creation_date": self.creation_date,
            "content": self.content,
            "tldr": self.tldr,
            "series_title": str(self.series_title),
            "post_url": self.post_url,
            "featured_post": self.featured_post
        }

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {

            }
        }


class Series(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    series_name: Optional[str] = Field(...,
                                       title="Blog series name, if part of a series")

    series_posts: list = Field(
        title="Blog series posts, if part of a series", required=False)

    def series_data(self):
        return {
            "series_name": self.series_name,
            "series_posts": self.series_posts}

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {


            }
        }


class FeaturedPosts(Blog):

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {


            }
        }


class BlogCategory(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    category_name: str = Field(...,
                               title="Blog Category Name")

    def category_data(self):
        return {
            "category_name": self.category_name}

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


class BlogList(BaseModel):
    blog_posts: List[Blog]
    featured_posts: List[Blog]
