import pytest
from main.data_types.event import Event


def test_event_initialization():
    """
    Test the initialization of the Event class.
    """
    event = Event()
    assert isinstance(event, Event)
    assert isinstance(event._callbacks, list)


def test_event_subscribe_int():
    """
    Test the subscribe method of the Event class with an integer data type.
    """
    event = Event()
    test_value = 42

    def callback_function(value: int):
        assert value == test_value
        
    event.subscribe(callback_function)
    assert callback_function in event._callbacks
    assert event.invoke(test_value) is None


def test_event_subscribe_str():
    """
    Test the subscribe method of the Event class with a string data type.
    """
    event = Event()
    test_value = "Hello, World!"

    def callback_function(value: str) -> bool:
        assert value == test_value

    event.subscribe(callback_function)
    assert callback_function in event._callbacks
    assert event.invoke(test_value) is None


def test_event_unsubscribe():
    """
    Test the unsubscribe method of the Event class.
    """
    event = Event()
    test_value = 42

    def callback_function(value: int):
        # Should not enter this block.
        assert False

    event.subscribe(callback_function)
    assert callback_function in event._callbacks
    event.unsubscribe(callback_function)

    assert callback_function not in event._callbacks
    assert len(event._callbacks) == 0
    assert event.invoke(test_value) is None


def test_event_invoke_multiple_subscribers():
    """
    Test the invoke method of the Event class with multiple subscribers.
    """
    event = Event()
    test_value1 = 42
    test_value2 = 43
    test_value3 = 44

    def callback_function1(value: int):
        assert value == test_value1

    def callback_function2(value: int):
        assert value != test_value2

    def callback_function3(value: int):
        assert value != test_value3

    event.subscribe(callback_function1)
    event.subscribe(callback_function2)
    event.subscribe(callback_function3)

    assert callback_function1 in event._callbacks
    assert callback_function2 in event._callbacks
    assert callback_function3 in event._callbacks
    assert event.invoke(test_value1) is None


def test_event_multiple_unsubscribe():
    """
    Test the unsubscribe method of the Event class with multiple subscribers.
    """
    event = Event()
    test_value = 42

    def callback_function(value: int):
        # Should not enter this block.
        assert False

    event.subscribe(callback_function)
    assert callback_function in event._callbacks
    event.unsubscribe(callback_function)
    assert callback_function not in event._callbacks
    assert len(event._callbacks) == 0

    with pytest.raises(ValueError):
        event.unsubscribe(callback_function)

    assert len(event._callbacks) == 0
    assert event.invoke(test_value) is None


def test_event_invoke_with_data_type():
    """
    Test the invoke method of the Event class with a custom data type.
    """
    
    class TestDataType:
        """Dummy TestDataType class."""
        def __init__(self, value: int) -> None:
            self.value = value
    event = Event()
    test_value = TestDataType(42)
    
    def callback_function(value: TestDataType):
        assert value.value == test_value.value

    event.subscribe(callback_function)
    assert callback_function in event._callbacks
    assert event.invoke(test_value) is None
