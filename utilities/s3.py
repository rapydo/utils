# -*- coding: utf-8 -*-

from utilities.logs import get_logger
log = get_logger(__name__)

try:
    import boto3
    import botocore
except ImportError as e:
    log.exit("\nThis module requires an extra package:\n%s", e)


class S3(object):
    """ wrapper for boto3 calls to S3 AWS-like spaces """

    _space_type = 's3'

    def __init__(self, space_url, space_region, bucket_name):
        self.session = boto3.session.Session()
        self.url = space_url
        self.client = self.session.client(
            self._space_type,
            endpoint_url=self.url,
            region_name=space_region,
        )
        self.bucket = bucket_name

    def pull(self, remote_path, local_path):
        try:
            self.client.download_file(self.bucket, remote_path, local_path)
        except botocore.exceptions.ClientError as e:
            if e.response.get('Error', {}).get('Code', 0) == "404":
                log.error("Object '%s' does not exist.", remote_path)
                return False
            else:
                raise
        else:
            log.debug(
                'File "%s": obtained\n\t%s' % (
                    remote_path, local_path
                )
            )
        return True

    def push(self, local_path, remote_path):
        self.client.upload_file(local_path, self.bucket, remote_path)
        log.debug(
            'File "%s": uploaded\n\t%s/%s' % (
                local_path, self.url, remote_path
            )
        )

    def matching_objects(self, prefix='', suffix=''):
        """
        src: https://alexwlchan.net/2018/01/listing-s3-keys-redux/
        """

        kwargs = {'Bucket': self.bucket}

        # If the prefix is a single string (not a tuple of strings), we can
        # do the filtering directly in the S3 API.
        if isinstance(prefix, str):
            kwargs['Prefix'] = prefix

        while True:

            # The S3 API response is a large blob of metadata.
            # 'Contents' contains information about the listed objects.
            resp = self.client.list_objects_v2(**kwargs)

            try:
                contents = resp['Contents']
            except KeyError:
                return

            for obj in contents:
                key = obj['Key']
                if key.startswith(prefix) and key.endswith(suffix):
                    yield obj

            # The S3 API is paginated, returning up to 1000 keys at a time.
            # Pass the continuation token into the next response, until we
            # reach the final page (when this field is missing).
            try:
                kwargs['ContinuationToken'] = resp['NextContinuationToken']
            except KeyError:
                break

    # def matching_keys(bucket, prefix='', suffix=''):
    #     for obj in get_matching_s3_objects(bucket, prefix, suffix):
    #         yield obj['Key']
