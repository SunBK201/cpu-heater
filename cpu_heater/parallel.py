import concurrent.futures
import traceback
from collections.abc import Callable

from tqdm import tqdm


def multiprocess(item_list, worker_fn: Callable, max_workers: int | None = None, show_progress: bool = False) -> list:
    result_list = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
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


def multithreads(item_list, worker_fn, max_workers: int | None = None, show_progress: bool = False) -> list:
    result_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
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
