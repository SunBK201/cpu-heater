import concurrent.futures
import signal
import sys
import traceback
from collections.abc import Callable

from tqdm import tqdm


def multiprocess(item_list: list[tuple], worker_fn: Callable, max_workers: int | None = None, show_progress: bool = False) -> list:
    def worker_initializer():
        def handler(signum, frame):
            sys.exit(1)
        signal.signal(signal.SIGINT, handler)

    result_list = []
    with concurrent.futures.ProcessPoolExecutor(max_workers, initializer=worker_initializer) as executor:
        futures = [executor.submit(worker_fn, *item) for item in item_list]
        try:
            if show_progress:
                for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                    try:
                        result = future.result()
                    except TimeoutError as e:
                        traceback.print_exception(e)
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
                        traceback.print_exception(e)
                        continue
                    except Exception as e:
                        traceback.print_exception(e)
                        continue
                    result_list.append(result)
        except KeyboardInterrupt:
            signal.signal(signal.SIGINT, signal.SIG_IGN)
            executor.shutdown()
            sys.exit(1)
    return result_list


def multithreads(item_list: list[tuple], worker_fn, max_workers: int | None = None, show_progress: bool = False) -> list:
    result_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        futures = [executor.submit(worker_fn, *item) for item in item_list]
        if show_progress:
            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                try:
                    result = future.result()
                except TimeoutError as e:
                    traceback.print_exception(e)
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
                    traceback.print_exception(e)
                    continue
                except Exception as e:
                    traceback.print_exception(e)
                    continue
                result_list.append(result)
    return result_list
