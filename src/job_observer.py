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
        self._success_dependency_count = 0

        self._subjob_max_dependency_count = 0
        self._subjob_success_dependency_count = 0

        self._observers = []
        self._callbacks = []

    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, value):
        self._status = value
        self.updated()
    
    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self, value):
        self._message = value
        self.updated()

    @property
    def max_dependency_count(self):
        return self._max_dependency_count
    
    @max_dependency_count.setter
    def max_dependency_count(self, value):
        self._max_dependency_count = value
        self.updated()

    @property
    def success_dependency_count(self):
        return self._success_dependency_count
    
    @success_dependency_count.setter
    def success_dependency_count(self, value):
        self._success_dependency_count = value
        self.updated()

    @property
    def subjob_max_dependency_count(self):
        return self._subjob_max_dependency_count
    
    @subjob_max_dependency_count.setter
    def subjob_max_dependency_count(self, value):
        self._subjob_max_dependency_count = value
        self.updated()

    @property
    def subjob_success_dependency_count(self):
        return self._subjob_success_dependency_count
    
    @subjob_success_dependency_count.setter
    def subjob_success_dependency_count(self, value):
        self._subjob_success_dependency_count = value
        self.updated()

    def increment_success(self):
        self._success_dependency_count += 1
        self._subjob_success_dependency_count += 1
        self.updated()

    def set_attributes(self, **kwargs):
        for key, value in kwargs.items():
            key = "_" + key
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated()
        
    def notify_observers(self):
        for observer in self._observers:
            observer.update(self)

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_callbacks(self):
        for callback in self._callbacks:
            callback(self.as_dict())

    def register_callback(self, callback):
        self._callbacks.append(callback)
    
    def unregister_callback(self, callback):
        self._callbacks.remove(callback)

    def updated(self):
        self.notify_callbacks()
        self.notify_observers()

    def as_dict(self):
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
    def update(self, job_model):
        print(job_model.as_dict())
