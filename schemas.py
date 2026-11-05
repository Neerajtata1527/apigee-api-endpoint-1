from pydantic import BaseModel, ConfigDict, Field


class EmployeeFields(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    department: str = Field(min_length=1, max_length=100)
    salary: float = Field(ge=0)


class EmployeeCreate(EmployeeFields):
    pass


class EmployeeReplace(EmployeeFields):
    """PUT requires the complete replaceable representation."""
    pass


class EmployeePatch(BaseModel):
    """PATCH accepts any non-empty subset of employee fields."""
    name: str | None = Field(default=None, min_length=1, max_length=120)
    department: str | None = Field(default=None, min_length=1, max_length=100)
    salary: float | None = Field(default=None, ge=0)

    model_config = ConfigDict(extra="forbid")


class EmployeeRead(EmployeeFields):
    id: int

    model_config = ConfigDict(from_attributes=True)
