from dataclasses import dataclass

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
        # Validate the 'name' attribute
        if not isinstance(self.name, str):
            raise TypeError(
                "Expected instance of type 'str' for attribute 'name',"
                f"but got '{type(self.name).__name__}'."
            )

        # Validate the 'port' attribute
        if not isinstance(self.port, int):
            raise TypeError(
                "Expected instance of type 'int' for attribute 'port',"
                f" but got '{type(self.port).__name__}'."
            )
        if not (0 <= self.port <= 65535):  # standard port range for TCP/UDP
            raise ValueError(
                "Invalid 'port' value. Expected a number between 0 and 65535, "
                f"but got '{self.port}'."
            )

        # Validate the 'enabled' attribute
        if not isinstance(self.enabled, bool):
            raise TypeError(
                "Expected instance of type 'bool' for attribute 'enabled',"
                f" but got '{type(self.enabled).__name__}'."
            )