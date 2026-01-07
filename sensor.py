"""Platform for sensor integration."""

from __future__ import annotations

import struct

import serial

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    timedelta,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from . import sondbus

SCAN_INTERVAL = timedelta(seconds=5)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""
    connection = serial.Serial("/dev/ttyACM0", baudrate=1000000)

    add_entities([ExampleSensor(connection)])


class ExampleSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Example Temperature"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, connection: serial.Serial) -> None:
        super().__init__()

        self.bus = sondbus.Master(connection)

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        for _ in range(100):
            self.bus.sync()

        data = self.bus.read_logical(0, 0, 4)
        value = struct.unpack("<f", data)[0]

        self._attr_native_value = value
