# Octox Labs Python SDK
py-octoxlabs is an API client for Octox Labs Cyber Security Asset Management platform on python programming language.

## Installation
```shell
pip install octoxlabs
```

## Getting Started
1. Go to settings
2. Click "Add User" button
3. Type Username and choose User Type as "API User"
4. Click "Create" button
5. Click your user's Edit button
6. Copy API Token

## Quick Start

```python
from octoxlabs import OctoxLabs

octo = OctoxLabs(ip="<your-octoxlabs-platform-ip>", token="<your-api-token>")
count, assets = octo.search_devices(query="Adapters = active-directory")
```

## Contributing
Also see; [CONTRIBUTING.md](CONTRIBUTING.md)