"""Common functions"""

import hashlib
import os
import requests
from tqdm import tqdm


DATA_CACHE_DIR = "data"


def download_file(url: str, filepath: str, chunk_size=1024):
    """Helper function to download a file from a given url"""
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get("content-length", 0))
    with open(filepath, "wb") as output_file, tqdm(
        desc=filepath,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = output_file.write(data)
            bar.update(size)


# an adapter which makes the multipart-generator issued by poster accessable to requests
# based upon code from http://stackoverflow.com/a/13911048/1659732
class FileProgressAdapter(object):
    def __init__(self, file_handle, file_size, progress):
        self.file_handle = file_handle
        self.length = file_size
        self.progress = progress

    def read(self, size=-1):
        self.progress(size)
        return self.file_handle.read(size)

    def __len__(self):
        return self.length


def upload_file(filepath: str, url: str):
    """Helper function to download a file from a given url"""
    total = os.path.getsize(filepath)
    with open(filepath, "rb") as input_file, tqdm(
        desc=filepath,
        total=total,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        resp = requests.put(
            url,
            data=FileProgressAdapter(input_file,
                                     total,
                                     lambda size: bar.update(size)
        ))


def md5_checksum(filepath: str):
    return hashlib.md5(open(filepath,'rb').read()).hexdigest()