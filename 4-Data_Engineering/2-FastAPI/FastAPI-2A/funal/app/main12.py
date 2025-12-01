from pydantic import BaseModel, EmailStr, ValidationError, model_validator


class Register(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str

    @model_validator(mode="after")  # after validation is more type safe
    def check_passwords(cls, values):
        if values.password != values.password_confirmation:
            raise ValueError("Oops! Passwords don't match")
        return values


# Passwords not matching
try:
    Register(
        email="aromerov@faculty.ie.edu", password="Hello", password_confirmation="Bye"
    )
except ValidationError as e:
    print(str(e))

# Ok
registered = Register(
    email="aromerov@faculty.ie.edu", password="Hello", password_confirmation="Hello"
)

print(registered)
