import cpu_heater


def adder(x, y):
    return x + y


def test_cpu_heater():
    item_list = [(i, i) for i in range(114514)]
    results = cpu_heater.multiprocess(item_list, adder, max_workers=8, show_progress=True)
    assert sorted(results) == sorted([i + i for i in range(114514)])


if __name__ == '__main__':
    test_cpu_heater()
