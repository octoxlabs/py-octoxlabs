# Octox Labs Python SDK
py-octoxlabs is an API client for Octox Labs Cyber Security Asset Management platform on python programming language.

## Installation
```shell
pip install octoxlabs
```

## Quick Start
```python
from octoxlabs import OctoxLabs

octo = OctoxLabs(ip="<your-octoxlabs-platform-ip>", token="<your-api-token>")
count, assets = octo.search_assets(query="Adapters = active-directory")
```
