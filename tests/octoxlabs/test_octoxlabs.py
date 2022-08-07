# Octoxlabs
from octoxlabs import OctoxLabs


def test_octoxlabs_init():
    octoxlabs = OctoxLabs(ip="octoxlabs.test", token="octoxlabs")

    assert octoxlabs.service.ip == "octoxlabs.test"
    assert octoxlabs.service.token == "octoxlabs"
