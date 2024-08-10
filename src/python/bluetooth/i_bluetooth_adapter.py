
from abc import ABC, abstractmethod

class IBluetoothAdapter(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def read_data(self):
        pass

    @abstractmethod
    async def write_data(self, data):
        pass