from dataclasses import dataclass
from typing import Any


@dataclass
class TransmitPortSetting:
    """
    再送信先のポートのデータを保持する

    Parameters
    ---------
    name: str
        ポートの名称
    port: int
        ポート番号
    enable: bool
        そのポートに再送信するかどうか
    """

    name: str
    port: int
    enabled: bool

    def __post_init__(self):
        self.validate_name(self.name)
        self.validate_port(self.port)
        self.validate_enabled(self.enabled)

    def __setattr__(self, key: str, value: Any) -> None:
        """
        各値のsetattr

        Parameters
        ---------
        key: str
            "name" | "port" | "enable"
        value: any
            代入したい値
        """
        validate_methoad = getattr(self, f"validate_{key}", None)
        if validate_methoad:
            value = validate_methoad(value)
        super().__setattr__(key, value)

    @staticmethod
    def validate_name(name):
        """
        nameを評価する
        int, floatの場合はstrに変換

        Parameters
        ---------
        name: str | int | float

        Returns
        ---------
        name: str
        """
        if isinstance(name, (int, float)):
            return str(name)
        elif not isinstance(name, str):
            raise TypeError(
                "Expected instance of type 'str' for attribute 'name',"
                f"but got '{type(name).__name__}'."
            )

    @staticmethod
    def validate_port(port):
        """
        portを評価する

        Parameters
        ---------
        port: int
            0 ~ 65535

        Returns
        ---------
        port: int
        """
        if not isinstance(port, int):
            raise TypeError(
                "Expected instance of type 'int' for attribute 'port',"
                f" but got '{type(port).__name__}'."
            )
        if not (0 <= port <= 65535):  # standard port range for TCP/UDP
            raise ValueError(
                "Invalid 'port' value. Expected a number between 0 and 65535, "
                f"but got '{port}'."
            )
        return port

    @staticmethod
    def validate_enabled(enabled):
        """
        enableを評価する

        Parameters
        ---------
        enable: bool

        Returns
        ---------
        enable: bool
        """
        if not isinstance(enabled, bool):
            raise TypeError(
                "Expected instance of type 'bool' for attribute 'enabled',"
                f" but got '{type(enabled).__name__}'."
            )
        return enabled
