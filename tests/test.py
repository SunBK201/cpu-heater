import cpu_heater


def adder(x, y):
    return x + y


def test_cpu_heater():
    args_list = [(i, i) for i in range(114514)]
    results = cpu_heater.multiprocess(
        adder,
        args_list,
        max_workers=8,
        show_progress=True,
        desc="test",
        not_none=True,
        extend_mode=False,
    )
    assert sorted(results) == sorted([i + i for i in range(114514)])


if __name__ == "__main__":
    test_cpu_heater()
