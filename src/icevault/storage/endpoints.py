from icevault.enums import BaseUrlEnum


class StorageUrls(BaseUrlEnum):
    upload = "/api/storage/initiate-upload/"
    confirm = "/api/storage/confirm-upload/"