import time
from datetime import datetime

from pydantic import BaseModel

from fastapi import FastAPI


class TimeStamp(BaseModel):
    # Don't do this!!!
    # It won't work!
    my_timestamp: datetime = datetime.now()


app = FastAPI()

time1 = TimeStamp()  # datetime.now() is NOT EXECUTED AGAIN!!!
print(time1.my_timestamp)


time.sleep(1)  # Wait for a second

time2 = TimeStamp()  # datetime.now() is NOT EXECUTED AGAIN!!!
print(time2.my_timestamp)


print(time1.my_timestamp < time2.my_timestamp)  # False
