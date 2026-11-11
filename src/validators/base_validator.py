from abc import ABC, abstractmethod


class BaseValidator(ABC):
    """
    Common interface for all cash validators.

    Any validator added to the system should implement
    these methods.
    """

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def disable(self):
        pass

    @abstractmethod
    def poll(self):
        pass

    @abstractmethod
    def get_serial_number(self):
        pass

    @abstractmethod
    def get_firmware_version(self):
        pass

    @abstractmethod
    def get_dataset_version(self):
        pass