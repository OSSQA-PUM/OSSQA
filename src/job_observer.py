"""
This module defines the JobStatus enumeration,
JobModelSingleton class, and JobListener class.

The JobStatus enumeration represents the status of a job.

The JobModelSingleton class is a singleton class that manages job-related data
and notifications. It has attributes for the status, message
dependency counts, observers, and callbacks. It also provides methods for
updating the attributes, registering/unregistering observers and callbacks,
and notifying observers and callbacks.

The JobListener class is an observer that prints
the job model attributes when it is updated.
"""

from enum import StrEnum
from typing import Callable


class JobStatus(StrEnum):
    """
    Represents the status of a job.
    """
    INACTIVE = "Inactive"
    VALIDATING = "Validating"
    PARSING = "Parsing"
    DATABASE_FILTER = "Database Filter"
    SSF_LOOKUP = "SSF Lookup"
    ANALYZING_SCORE = "Analyzing Score"
    FINAL_SCORE = "Final Score"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class JobModelSingleton:
    """
    Represents a singleton class for managing job-related data
    and notifications.

    Attributes:
        _status (JobStatus): The status of the job.
        _message (str): The message associated with the job.
        _max_dependency_count (int): The maximum dependency count for the job.
        _success_dependency_count (int): The count of successfully completed
                                         dependencies for the job.
        _subjob_max_dependency_count (int): The maximum dependency count for
                                            subjobs.
        _subjob_success_dependency_count (int): The count of successfully
                                                completed dependencies for
                                                subjobs.
        _observers (list): A list of observers subscribed to receive updates.
        _callbacks (list): A list of callbacks to be called when the job is
                           updated.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self._status: JobStatus = JobStatus.INACTIVE
        self._message = ""
        self._max_dependency_count = 0
        self._success_dependency_count = 0

        self._subjob_max_dependency_count = 0
        self._subjob_success_dependency_count = 0

        self._observers = []
        self._callbacks = []

    @property
    def status(self) -> JobStatus:
        """
        Returns the status of the job.
        """
        return self._status

    @status.setter
    def status(self, value: JobStatus) -> None:
        self._status = value
        self.updated()

    @property
    def message(self) -> str:
        """
        Returns the message associated with the job.
        """
        return self._message

    @message.setter
    def message(self, value: str) -> None:
        self._message = value
        self.updated()

    @property
    def max_dependency_count(self) -> int:
        """
        Returns the maximum dependency count for the job.
        """
        return self._max_dependency_count

    @max_dependency_count.setter
    def max_dependency_count(self, value: int) -> None:
        self._max_dependency_count = value
        self.updated()

    @property
    def success_dependency_count(self) -> int:
        """
        Returns the count of successfully completed dependencies for the job.
        """
        return self._success_dependency_count

    @success_dependency_count.setter
    def success_dependency_count(self, value: int) -> None:
        self._success_dependency_count = value
        self.updated()

    @property
    def subjob_max_dependency_count(self) -> int:
        """
        Returns the maximum dependency count for subjobs.
        """
        return self._subjob_max_dependency_count

    @subjob_max_dependency_count.setter
    def subjob_max_dependency_count(self, value: int) -> None:
        self._subjob_max_dependency_count = value
        self.updated()

    @property
    def subjob_success_dependency_count(self) -> int:
        """
        Returns the count of successfully completed dependencies for subjobs.
        """
        return self._subjob_success_dependency_count

    @subjob_success_dependency_count.setter
    def subjob_success_dependency_count(self, value: int) -> None:
        self._subjob_success_dependency_count = value
        self.updated()

    def increment_success(self) -> None:
        """
        Increments the count of successfully completed dependencies for the job
        and subjob.
        """
        self._success_dependency_count += 1
        self._subjob_success_dependency_count += 1
        self.updated()

    def set_attributes(self, **kwargs) -> None:
        """
        Sets the attributes of the object based on the provided keyword
        arguments.

        Args:
            **kwargs: Keyword arguments representing the attributes to be set.
        """
        for key, value in kwargs.items():
            key = "_" + key
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated()

    def notify_observers(self) -> None:
        """
        Notifies all observers by calling their update method with the current
        instance.
        """
        for observer in self._observers:
            observer.update(self)

    def register_observer(self, observer) -> None:
        """
        Registers an observer to receive updates.

        Args:
            observer: The observer object to be registered.
        """
        self._observers.append(observer)

    def unregister_observer(self, observer) -> None:
        """
        Removes the specified observer from the list of observers.

        Args:
            observer: The observer to be removed.
        """
        self._observers.remove(observer)

    def notify_callbacks(self) -> None:
        """
        Notifies all callbacks by calling them with the current instance dict:.
        """
        for callback in self._callbacks:
            callback(self.as_dict())

    def register_callback(self, callback: Callable) -> None:
        """
        Registers a callback to be called when the job is updated.

        Args:
            callback: The callback function to be registered.
        """
        self._callbacks.append(callback)

    def unregister_callback(self, callback: Callable) -> None:
        """
        Removes the specified callback from the list of callbacks.

        Args:
            callback: The callback to be removed.
        """
        self._callbacks.remove(callback)

    def updated(self) -> None:
        """
        Notifies all observers and callbacks that the job has been updated.
        """
        self.notify_callbacks()
        self.notify_observers()

    def as_dict(self) -> dict:
        """
        Returns the job attributes as a dictionary.

        Returns:
            dict: The job attributes as a dictionary.
        """
        return {
            "job_status": self._status.value,
            "job_message": self._message,
            "max_dependency_count": self._max_dependency_count,
            "success_dependency_count": self._success_dependency_count,
            "subjob_max_dependency_count": self._subjob_max_dependency_count,
            "subjob_success_dependency_count":
                self._subjob_success_dependency_count
        }


class JobListerner:
    """
    Represents an observer that prints the job model attributes when it is
    updated.
    """
    def update(self, job_model: JobModelSingleton) -> None:
        """
        Prints the job model attributes when it is updated.

        Args:
            job_model (JobModelSingleton): The job model instance.
        """
        print(job_model.as_dict())
