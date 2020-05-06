from abc import abstractmethod
from typing import Dict


class BaseElement:
    @abstractmethod
    def to_dict(self) -> Dict:
        raise NotImplementedError('You did not implement FbApi.to_dict() method')


class BaseTemplate:
    @abstractmethod
    def to_json_message(self) -> Dict:
        raise NotImplementedError('You did not implement FbApi.to_dict() method')
