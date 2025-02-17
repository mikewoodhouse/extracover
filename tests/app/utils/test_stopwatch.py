from app.utils import StopWatch


def test_elapsed_formatting():
    with StopWatch(decimals=2) as sw:
        rtn = sw.formatted(sw.elapsed)
        parts = rtn.split(".")
        assert len(parts) == 2
        assert len(parts[1]) == 2
