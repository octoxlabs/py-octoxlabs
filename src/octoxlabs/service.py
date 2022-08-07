# Standard Library
import os
from typing import Dict, Union

# Third Party
import urllib3
import requests

# Local Folder
from .exceptions import ApiException

urllib3.disable_warnings()


class OctoxLabsService:
    ip: str
    base_url: str

    token: str
    token_prefix: str = "Octoxlabs"

    headers: Dict[str, str]

    def __init__(self, ip: str, token: str):
        self.set_ip(ip=ip)
        self.set_token(token=token)

    def set_ip(self, ip: str):
        self.ip = ip
        self.base_url = os.getenv("OCTOXLABS_URL", None) or f"https://{self.ip}:8043"

    def set_token(self, token: str):
        self.token = token
        self.headers = {"Authorization": f"{self.token_prefix} {self.token}"}

    def request_builder(
        self,
        path: str,
        method: str = "GET",
        params: Dict[str, Union[str, int]] = None,
        **kwargs,
    ):
        response = requests.request(
            method=method.upper(),
            url=f"{self.base_url}{path}",
            params=params,
            headers=self.headers,
            verify=False,
            **kwargs,
        )
        if response.status_code > 299:
            raise ApiException(f"Status code: {response.status_code}. Response: {response.text}")
        return response
