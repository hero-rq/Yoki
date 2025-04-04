import uuid

class SmartDevice:
    def __init__(self, device_id, name, location):
        self.id = device_id or str(uuid.uuid4())
        self.name = name
        self.location = location
        self._status = "Inactive"

    def get_status(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "status": self._status
        }

    def get_id(self):
        return self.id

    def __str__(self):
        return f"{self.name} [{self.location}] :: {self._status}"


class SmartLight(SmartDevice):
    def __init__(self, device_id, name, location, is_on=False, brightness=100):
        super().__init__(device_id, name, location)
        self._is_on = is_on
        self._brightness = max(0, min(brightness, 100))
        self._refresh()

    def _refresh(self):
        self._status = f"Light {'ON' if self._is_on else 'OFF'}, Brightness: {self._brightness}%"

    def turn_on(self):
        self._is_on = True
        self._refresh()

    def turn_off(self):
        self._is_on = False
        self._refresh()

    def toggle(self):
        self._is_on = not self._is_on
        self._refresh()

    def set_brightness(self, level):
        self._brightness = max(0, min(int(level), 100))
        self._refresh()

    def get_status(self):
        data = super().get_status()
        data.update({"is_on": self._is_on, "brightness": self._brightness})
        return data


class SmartThermostat(SmartDevice):
    MODES = {"Off", "Heat", "Cool", "Auto"}

    def __init__(self, device_id, name, location, current_temp=70.0, target_temp=72.0, mode="Off"):
        super().__init__(device_id, name, location)
        self._current_temp = float(current_temp)
        self._target_temp = float(target_temp)
        self._mode = mode if mode in self.MODES else "Off"
        self._is_running = False
        self._refresh()

    def _refresh(self):
        active = "Running" if self._is_running else "Idle"
        self._status = f"{self._mode} Mode - {active} - {self._current_temp}/{self._target_temp}F"

    def set_target_temperature(self, temp):
        self._target_temp = float(temp)
        self._evaluate()

    def set_mode(self, mode):
        if mode in self.MODES:
            self._mode = mode
            self._evaluate()

    def update_ambient_temperature(self, temp):
        self._current_temp = float(temp)
        self._evaluate()

    def _evaluate(self):
        self._is_running = False
        if self._mode == "Heat" and self._current_temp < self._target_temp:
            self._is_running = True
        elif self._mode == "Cool" and self._current_temp > self._target_temp:
            self._is_running = True
        elif self._mode == "Auto":
            delta = self._target_temp - self._current_temp
            self._is_running = abs(delta) > 1
        self._refresh()

    def get_status(self):
        data = super().get_status()
        data.update({
            "current_temperature": self._current_temp,
            "target_temperature": self._target_temp,
            "mode": self._mode,
            "is_running": self._is_running
        })
        return data


class DeviceHub:
    def __init__(self):
        self._devices = {}

    def connect(self, device):
        if not isinstance(device, SmartDevice):
            return
        if device.get_id() in self._devices:
            return
        self._devices[device.get_id()] = device

    def get(self, device_id):
        return self._devices.get(device_id)

    def all_devices(self):
        return list(self._devices.values())

    def by_location(self, location):
        return [d for d in self._devices.values() if d.location == location]

    def status_report(self):
        print("\n=== SMART HOME STATUS REPORT ===")
        for device in self._devices.values():
            print(device)
        print("================================\n")


hub = DeviceHub()

light1 = SmartLight("A1", "Ceiling Light", "Living Room")
light2 = SmartLight("B2", "Table Lamp", "Bedroom", is_on=True, brightness=40)
thermostat = SmartThermostat("C3", "Nest Thermostat", "Hallway", current_temp=68, target_temp=72, mode="Auto")

hub.connect(light1)
hub.connect(light2)
hub.connect(thermostat)

hub.status_report()

light1.turn_on()
light1.set_brightness(60)
light2.toggle()
thermostat.update_ambient_temperature(66)
thermostat.set_mode("Heat")
hub.status_report()
