from __future__ import annotations

import concurrent.futures
import signal
import sys
import traceback
from collections.abc import Callable

from tqdm import tqdm


class Timing:
    def __init__(self, func: Callable, timeout: int) -> None:
        self.func = func
        self.timeout = timeout

    @staticmethod
    def handler(signum, frame):
        raise TimeoutError

    def __call__(self, *args, **kwargs):
        signal.signal(signal.SIGALRM, self.handler)
        signal.alarm(self.timeout)
        return self.func(*args, **kwargs)


def __worker_initializer():
    def handler(signum, frame):
        sys.exit(1)

    signal.signal(signal.SIGINT, handler)


def multiprocess(
    worker_fn: Callable,
    args_list: list[tuple],
    max_workers: int | None = None,
    show_progress: bool = False,
    timeout: int | None = None,
) -> list:
    worker_fn = Timing(worker_fn, timeout) if timeout else worker_fn
    result_list = []
    with concurrent.futures.ProcessPoolExecutor(
        max_workers, initializer=__worker_initializer
    ) as executor:
        futures = [executor.submit(worker_fn, *item) for item in args_list]
        try:
            if show_progress:
                for future in tqdm(
                    concurrent.futures.as_completed(futures), total=len(futures)
                ):
                    try:
                        result = future.result()
                    except TimeoutError as e:
                        continue
                    except Exception as e:
                        traceback.print_exception(e)
                        continue
                    result_list.append(result)
            else:
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                    except TimeoutError as e:
                        continue
                    except Exception as e:
                        traceback.print_exception(e)
                        continue
                    result_list.append(result)
        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            executor.shutdown()
            sys.exit(1)
        except Exception as e:
            traceback.print_exception(e)
    return result_list


def multithreads(
    worker_fn: Callable,
    args_list: list[tuple],
    max_workers: int | None = None,
    show_progress: bool = False,
) -> list:
    result_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        futures = [executor.submit(worker_fn, *item) for item in args_list]
        try:
            if show_progress:
                for future in tqdm(
                    concurrent.futures.as_completed(futures), total=len(futures)
                ):
                    try:
                        result = future.result()
                    except TimeoutError as e:
                        continue
                    except Exception as e:
                        traceback.print_exception(e)
                        continue
                    result_list.append(result)
            else:
                for future in concurrent.futures.as_completed(futures):
                    try:
                        result = future.result()
                    except TimeoutError as e:
                        continue
                    except Exception as e:
                        traceback.print_exception(e)
                        continue
                    result_list.append(result)
        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            executor.shutdown()
            sys.exit(1)
        except Exception as e:
            traceback.print_exception(e)
    return result_list
