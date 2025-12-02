from fastapi import FastAPI, Header

app = FastAPI()


# We use the Header function to get the user-agent header
# We don't know how it handles the operations needed

# It's like calling "Header, do your things and give me the user-agent"


@app.get("/")
async def my_header(user_agent: str = Header(...)):
    return {"user_agent": user_agent}
