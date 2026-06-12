from icevault.enums import BaseUrlEnum


class ArchiveUrls(BaseUrlEnum):
    filter = "/api/archives/"
    preview = "/api/archives/{uuid}/preview/"
    restore = "/api/archives/{uuid}/restore/"
    download = "/api/archives/{uuid}/download/"
    delete = "/api/archives/{uuid}/"
    patch = "/api/archives/{uuid}/"
    cancel_deletion = "/api/archives/{uuid}/cancel-deletion/"
