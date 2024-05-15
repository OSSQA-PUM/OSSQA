"""
This module defines the Event class, which allows subscribing to and invoking
callback functions.

Example usage:
    event = Event[int]()
    event.subscribe(callback_function)
    event.invoke(42)
"""

from typing import TypeVar, Generic, Callable, Any


T = TypeVar('T')


class Event(Generic[T]):
    """
    Represents an event that can be subscribed to and invoked.

    Attributes:
        _callbacks (list[Callable[[T], Any]]): A list of callback functions 
        subscribed to the event.
    """

    _callbacks: list[Callable[[T], Any]]

    def __init__(self) -> None:
        """
        Initializes a new instance of the Event class.
        """
        self._callbacks = []

    def subscribe(self, callback: Callable[[T], Any]) -> None:
        """
        Subscribes to the event.

        Args:
            callback (Callable[[T], Any]): The callback function to subscribe.
        """
        self._callbacks.append(callback)

    def unsubscribe(self, callback: Callable[[T], Any]) -> None:
        """
        Unsubscribes from the event.

        Args:
            callback (Callable[[T], Any]): The callback function to 
                                           unsubscribe.
        """
        try:
            self._callbacks.remove(callback)
        except ValueError as e:
            raise ValueError(f"Callback {callback} not in list") from e

    def invoke(self, event_data: T) -> None:
        """
        Invokes the callback functions of subscribers.

        Args:
            event_data (T): The value to pass as an argument to the 
            callback functions.
        """
        for callback in self._callbacks:
            callback(event_data)
