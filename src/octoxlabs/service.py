# Standard Library
import os
from typing import Dict, Union

# Third Party
import urllib3
import requests

# Local Folder
from .exceptions import ApiException
from .constants.paths import access_token_path

urllib3.disable_warnings()


class OctoxLabsService:
    ip: str
    base_url: str

    token: str
    access_token: str
    token_prefix: str = "Bearer"

    http_proxy: str = None
    https_proxy: str = None
    no_verify: bool = True

    headers: Dict[str, str] = None

    def __init__(self, ip: str, token: str, http_proxy: str = None, https_proxy: str = None, no_verify: bool = True):
        self.set_ip(ip=ip)
        self.set_token(token=token)
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy
        self.no_verify = no_verify

    def set_ip(self, ip: str):
        self.ip = ip
        self.base_url = os.getenv("OCTOXLABS_URL", None) or f"https://{self.ip}:8443"

    def set_token(self, token: str):
        self.token = token
        self.access_token = self.request_builder(
            method="POST", path=access_token_path(), json={"token": self.token}
        ).json()["access"]
        self.headers = {"Authorization": f"{self.token_prefix} {self.access_token}"}

    @staticmethod
    def set_proxies(http_proxy: str = None, https_proxy: str = None):
        proxy = {}
        if http_proxy:
            proxy["http"] = http_proxy
        if https_proxy:
            proxy["https"] = https_proxy
        return proxy

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
            verify=False if self.no_verify else True,
            proxies=self.set_proxies(http_proxy=self.http_proxy, https_proxy=self.https_proxy),
            **kwargs,
        )
        if response.status_code > 299:
            raise ApiException(f"Status code: {response.status_code}. Response: {response.text}")
        return response
