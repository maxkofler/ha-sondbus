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

SCAN_INTERVAL = timedelta(seconds=10)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the sensor platform."""

    add_entities([VorlaufSensor()])


class VorlaufSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Temperatur Vorlauf"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    unique_id = "vorlauf"

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        connection = serial.Serial("/dev/ttyACM0", baudrate=1000000)
        bus = sondbus.Master(connection)

        for _ in range(100):
            bus.sync()

        data = bus.read_logical(0, 0, 4)
        value = struct.unpack("<f", data)[0]

        self._attr_native_value = value


class RuecklaufSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Temperatur Ruecklauf"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    unique_id = "ruecklauf"

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """

        connection = serial.Serial("/dev/ttyACM0", baudrate=1000000)
        bus = sondbus.Master(connection)

        for _ in range(100):
            bus.sync()

        data = bus.read_logical(0, 4, 4)
        value = struct.unpack("<f", data)[0]

        self._attr_native_value = value
