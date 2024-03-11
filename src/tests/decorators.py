"""
Decorator that are useful for testing.
"""

import logging
from decorator import decorator


def __log_success(module_name: str,
                  function_name: str,
                  test_case_ids: list[int]):
    if test_case_ids:
        test_case_str = ",".join(f"TF{i}" for i in test_case_ids)
    else:
        test_case_str = "N/A"

    logging.info(
        "\n\tModule: %s\n\tFunction: %s\n\tTest cases: %s\n\tResult: SUCCESS\n",
        module_name,
        function_name,
        test_case_str,
    )


def __log_failure(module_name: str,
                  function_name: str,
                  test_case_ids: list[int],
                  error: AssertionError):
    if test_case_ids:
        test_case_str = ",".join(f"TF{i}" for i in test_case_ids)
    else:
        test_case_str = "N/A"

    # error_str aligns lines with each other
    error_str = "\n\t       ".join(str(error).split("\n"))

    logging.info(
        "\n\tModule: %s\n\tFunction: %s\n\tTest cases: %s\n\tResult: FAILURE\n\tCause: %s\n",
        module_name,
        function_name,
        test_case_str,
        error_str,
    )


def log_test_results(test_case_ids: list[int]):
    """
    Logs the results of a test.

    Args:
        test_case_id (list[int]): The associated test case IDs.
    """
    def deco(func):
        def wrapper(func, *args, **kwargs):
            try:
                result = func(*args, **kwargs)
                __log_success(func.__module__, func.__name__, test_case_ids)
                return result
            except AssertionError as error:
                __log_failure(func.__module__, func.__name__, test_case_ids,
                              error)
                raise error  # Re-raise error so that pytest catches it
        return decorator(wrapper, func)
    return deco
