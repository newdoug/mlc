import dataclass as dc


@dc.dataclass
class SettingsBase:
    """Base settings class"""

    def asdict(self) -> dict:
        """Return settings as a dict"""
        return dc.asdict(self)
