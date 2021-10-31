import pydantic


class Skill(pydantic.BaseModel):
    name: str


class HeroClass(pydantic.BaseModel):
    name: str


class Blueprint(pydantic.BaseModel):
    name: str

    @classmethod
    def get_by_name(cls, name):
        return cls(name=name)
