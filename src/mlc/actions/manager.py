"""Action manager"""

from abc import abstractmethod
from typing import Any, Callable


class Action:
    """A particular piece of work. An action"""

    def __init__(self):
        self.instance_results = []

    @abstractmethod
    def _run(self, data, action_config: dict) -> Any:
        raise NotImplementedError("Must implement action _run method")

    def run(self, data, action_config: dict) -> Any:
        """Public run method. Should not be overriden by subclasses"""
        result = self._run(data, action_config)
        self.instance_results.append(result)
        return result


class Rc4EncryptAction(Action):
    def _run(self, data, action_config: dict) -> Any:
        return f"RC4({data})"


class LzmaCompressAction(Action):
    def _run(self, data, action_config: dict) -> Any:
        return f"LZMA({data})"


class ActionManager:
    """Managers actions"""

    def __init__(self):
        self.registered_actions = {}
        self.loaded_actions = {}

    def register_action(self, name: str, action: Action, override: bool = False) -> None:
        """Register an action with an action name.
        Raises `ValueError` if `name` is already registered unless `override`
        is `True`.
        """
        if not override and name in self.registered_actions:
            raise ValueError(f"Action named '{name}' already registered with function '{function}'")
        self.registered_actions[name] = function

    def unregister_action(self, name: str, not_exist_ok: bool = False) -> None:
        """Unregister an action.
        Raises `ValueError` if the given action `name` is not registered
        unless `not_exist_ok` is `True`.
        """
        # if not not_exist_ok and name not in self.registered_actions:
        if name in self.registered_actions:
            self.registered_actions.pop(name)
        elif not not_exist_ok:
            raise ValueError(f"Action named '{name}' is not registered")

    def run_action_instance(self, action_config: dict) -> Any:
        """Runs action with name `name`, passing `settings` as an argument"""
        name = action_config["name"]
        if name not in self.registered_actions:
            raise ValueError(f"Action named '{name}' is not registered")
        settings = action_config["settings"]
        for sub_action in action_config.get("actions", []):
            self.run_action_instance(sub_action)
        return self.registered_actions[name](settings)
