# Octoxlabs
from octoxlabs.models.discovery import Discovery


class DiscoveryFactory:
    @staticmethod
    def create(
        id=1,
        start_time="2021-07-19T00:23:28.752662Z",
        end_time="2021-07-19T00:23:28.752662Z",
        status=2,
        progress=100.0,
    ):
        return Discovery(id=id, start_time=start_time, end_time=end_time, status=status, progress=progress)
