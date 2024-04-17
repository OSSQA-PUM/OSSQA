from enum import StrEnum


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

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self,):
        self._status: JobStatus = JobStatus.INACTIVE
        self._message = ""
        self._max_dependency_count = 0
        self._current_dependency_count = 0
        self._observers = []

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, status: JobStatus):
        if not isinstance(status, JobStatus):
            raise ValueError("job_status must be an instance of JobStatus")
        self._status = status
        self.notify_observers()

    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self, message):
        self._message = message
        self.notify_observers()

    @property
    def max_dependency_count(self):
        return self._max_dependency_count
    
    @max_dependency_count.setter
    def max_dependency_count(self, max_dependency_count):
        self._max_dependency_count = max_dependency_count
        self.notify_observers()

    @property
    def current_dependency_count(self):
        return self._current_dependency_count
    
    @current_dependency_count.setter
    def current_dependency_count(self, current_dependency_count):
        self._current_dependency_count = current_dependency_count
        self.notify_observers()

    def set_attributes(
            self,
            status,
            message,
            max_dependency_count,
            current_dependency_count):
        self._status = status
        self._message = message
        self._max_dependency_count = max_dependency_count
        self._current_dependency_count = current_dependency_count
        self.notify_observers()
        
    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

    def register_observer(self, observer):
        self._observers.append(observer)

    def __dict__(self):
        return {
            "job_status": self._status.value,
            "job_message": self._message,
            "max_dependency_count": self._max_dependency_count,
            "current_dependency_count": self._current_dependency_count
        }


class JobListerner:
    def update(self, job_model):
        print(job_model.__dict__())
