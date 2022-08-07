def test_discovery_parsed_times(discovery_factory):
    discovery = discovery_factory.create()

    assert discovery.parsed_start_time.year == 2021
    assert discovery.parsed_start_time.month == 7
    assert discovery.parsed_start_time.day == 19
    assert discovery.parsed_start_time.hour == 0
    assert discovery.parsed_start_time.minute == 23
    assert discovery.parsed_start_time.second == 28
    assert discovery.parsed_start_time.microsecond == 752662
    assert discovery.parsed_end_time.microsecond == 752662
