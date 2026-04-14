from pydantic import BaseModel, Field
from typing import List, Tuple, Optional

class UserBase(BaseModel):
    Name: str
    location: Tuple[float, float]
    Budget: float
    Hobbies: str
    Is_Vegetarian: str
    mobile: int
    image: Optional[str] = ""

class UserCreate(UserBase):
    user: str

class UserOut(UserBase):
    user: str
    Distance: Optional[float] = None

class MatchResult(BaseModel):
    user: str
    Name: str
    Matching: str
    Distance: float
    location: str
    mobile: int
    image: str
    Budget: float
    Hobbies: str
    Is_Vegetarian: str
    budget_match: str
    diet_match: str
    hobby_match: str
    distance_match: str
