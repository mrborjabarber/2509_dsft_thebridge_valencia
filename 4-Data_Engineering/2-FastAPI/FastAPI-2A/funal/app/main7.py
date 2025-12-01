from datetime import datetime

from pydantic import BaseModel, Field

from fastapi import FastAPI

app = FastAPI()


def give_me_a_list():
    return ["a", "b", "c"]


class Model(BaseModel):
    my_list: list[str] = Field(
        default_factory=give_me_a_list
    )  # Notice that the functions in default_factory are not called till we initiate them in Model()

    my_datetime: datetime = Field(default_factory=datetime.now)
    my_other_list: list[str] = Field(default_factory=list)


object1 = Model()
print(object1.my_list)  # ["a", "b", "c"]
print(object1.my_other_list)  # []

object1.my_list.append("d")
print(object1.my_list)  # ["a", "b", "c", "d"]

object2 = Model()
print(object2.my_list)  # ["a", "b", "c"]
print(object2.my_other_list)  # []

print(object1.my_datetime < object2.my_datetimed)  # True
