## class diagram

```mermaid
classDiagram
class App
App : Duplicator duplicator
App : main()

class Duplicator
Duplicator : Setting settings
Duplicator : Queue queue
Duplicator : OscReceiver receiver
Duplicator : OscTransmitter transmitter
Duplicator : bool is_duplicate
Duplicator : start_duplicate()
Duplicator : stop_duplicate()
Duplicator : save_settings()

class OscReceiver
OscReceiver : int receive_port
OscReceiver : BlockingOSCUDPServer _server
OscReceiver : Queue _message_queue
OscReceiver : start()
OscReceiver : stop()
OscReceiver : message_handler()

class OscTransmitter
OscTransmitter : Queue q
OscTransmitter : dict _clients
OscTransmitter : Lock _clients_lock
OscTransmitter : Thread _thread
OscTransmitter : bool _running
OscTransmitter : start()
OscTransmitter : pause()
OscTransmitter : update_transmit_port()
OscTransmitter : _loop()
OscTransmitter : _transmit()


class Settings
Settings : int _receive_port
Settings : list transmit_port_settings
Settings : load_json()
Settings : save_json()
Settings : update_receive_port_settings()
Settings : add_transmit_port_settings()
Settings : remove_transmit_port_settings()
Settings : enable_transmit_port()
Settings : disable_transmit_port()

class TransmitPortSetting
TransmitPortSetting : str name
TransmitPortSetting : int port
TransmitPortSetting : bool enabled

App <-- Duplicator
Duplicator <-- Settings
Duplicator <-- OscReceiver
Duplicator <-- OscTransmitter
Settings *-- TransmitPortSetting
```