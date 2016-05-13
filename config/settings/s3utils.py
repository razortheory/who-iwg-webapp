from storages.backends.s3boto import S3BotoStorage


class MediaRootS3BotoStorage(S3BotoStorage):
    location = 'media'
    file_overwrite = False


class StaticRootS3BotoStorage(S3BotoStorage):
    location = 'static'
    file_overwrite = True
