from enum import StrEnum


class CaseInsensitiveStrEnum(
    StrEnum,
):
    """"""

    @classmethod
    def _missing_(
        cls,
        value: object,
    ) -> str | None:
        """"""
        assert isinstance(value, str)
        value: str = value.lower()

        for member in cls:
            if member.lower() == value:
                return member

        return None

class BaseUrlEnum(StrEnum):
    """"""

    def get_url(self, **kwargs):
        return self.value.format(**kwargs)

class StorageClassEnum(CaseInsensitiveStrEnum):
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    GLACIER_IR = "GLACIER_IR"
    STANDARD = "STANDARD"

class MethodEnum(CaseInsensitiveStrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
