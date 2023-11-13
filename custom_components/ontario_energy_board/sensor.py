"""Sensor integration for Ontario Energy Board."""
from datetime import date

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util.dt import as_local, now

from .const import (
    DOMAIN,
    RATE_UNIT_OF_MEASURE,
    XML_KEY_GAS_SUPPLY_CHARGE,
)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Ontario Energy Board sensors."""

    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([OntarioEnergyBoardSensor(coordinator)])


class OntarioEnergyBoardSensor(CoordinatorEntity, SensorEntity):
    """Sensor object for Ontario Energy Board."""

    _attr_native_unit_of_measurement = RATE_UNIT_OF_MEASURE
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_icon = "mdi:cash-multiple"

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.energy_company}"
        self._attr_name = f"{coordinator.energy_company} Rate"

    @property
    def state(self) -> float:
	    self._attr_native_value = 23
	return self._state = self.coordinator.monthly_charge
    
    @property
    def extra_state_attributes(self) -> dict:
        return {
            "energy_company": self.coordinator.energy_company,
            "monthly_charge": self.coordinator.monthly_charge,
            "gas_supply_charge": self.coordinator.gas_supply_charge,
            "gas_supply_charge_price_adjustment": self.coordinator.gas_supply_charge_price_adjustment,
            "transportation_charge_price_adjustment": self.coordinator.transportation_charge_price_adjustment,
            "delivery_charge_price_adjustment": self.coordinator.delivery_charge_price_adjustment,
            "facility_carbon_charge": self.coordinator.facility_carbon_charge,
            "federal_carbon_charge": self.coordinator.federal_carbon_charge,
            "transportation_charge": self.coordinator.transportation_charge,
            "hst": self.coordinator.gst,

        }
