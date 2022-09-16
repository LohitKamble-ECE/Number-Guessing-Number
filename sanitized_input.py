from typing import Any, Callable, Optional, Sequence


def sanitized_input(
    prompt: Optional[str] = None,
    expected_type: Optional[Callable[[str], Any]] = None,
    expected_values: Optional[Sequence[Any]] = None,
) -> Any:
    """
    Prompt the user to enter value(s).
    
    By default, it returns `str`, but you can ask for any other type.
    For instance, you can ask for a valid integer:
    ```
    >>> num = sanitized_input("Please enter a valid integer: ", int)
    Please enter a valid integer: 42
    >>> type(num)
    class <'int'>
    ```

    If `expected_values` provided then it test for membership.
    ```
    >>> fruit = sanitized_input("Please enter a fruit: ", str, ["apple", "orange", "peach"])
    please enter a fruit: banana
    ValueError: input must apple, orange or peach
    ```
    """
    user_response = input(prompt)

    if expected_type is not None:
        try:
            user_response = expected_type(user_response)
        except ValueError:
            raise TypeError(f"input type must be {expected_type.__name__}")
        else:
            if expected_values is not None and user_response not in expected_values:

                if len(expected_values) == 1:
                    expected_error = f"{expected_values[0]}"
                elif isinstance(expected_values, range):
                    if user_response < expected_values.start:
                        expected_error = (
                            f"greater than or equal to {expected_values.start}"
                        )
                    elif user_response >= expected_values.stop:
                        expected_error = f"less than {expected_values.stop}"
                    else:
                        if len(expected_values) > 5:
                            expected_error = f"in {', '.join(str(x) for x in expected_values[:5])} , ..., {expected_values[-1]}"
                        else:
                            expected_error = f"{' or '.join((', '.join(str(x) for x in expected_values[:-1]),str(expected_values[-1]),))}"
                else:
                    expected_error = f"be {' or '.join((', '.join(str(x) for x in expected_values[:-1]),str(expected_values[-1]),))}"
                raise ValueError(f"input must be {expected_error}")

    return user_response
