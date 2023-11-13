"""Utility methods used by the Ontario Energy Board integration.
"""
import async_timeout
import logging
import xml.etree.ElementTree as ET
from typing import Final

import holidays
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import Throttle

from .const import (
    DOMAIN,
    RATES_URL,
    REFRESH_RATES_INTERVAL,
    XML_KEY_MONTHLY_CHARGE,
    XML_KEY_GAS_SUPPLY_CHARGE,
    XML_KEY_GAS_SUPPLY_CHARGE_PRICE_ADJUSTMENT,
    XML_KEY_TRANSPORTATION_CHARGE_PRICE_ADJUSTMENT,
    XML_KEY_DELIVERY_CHARGE_PRICE_ADJUSTMENT,
    XML_KEY_FACILITY_CARBON_CHARGE,
    XML_KEY_FEDERAL_CARBON_CHARGE,
    XML_KEY_TRANSPORTATION_CHARGE,
    XML_KEY_GST,
)


_LOGGER: Final = logging.getLogger(__name__)


class OntarioEnergyBoardDataUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to manage Ontario Energy Board data."""

    _timeout = 10
    monthly_charge = None
    gas_supply_charge = None
    gas_supply_charge_price_adjustment = None
    transportation_charge_price_adjustment = None
    delivery_charge_price_adjustment = None
    facility_carbon_charge = None
    federal_carbon_charge = None
    transportation_charge = None
    gst = None


    def __init__(self, hass: HomeAssistant) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=REFRESH_RATES_INTERVAL,
            update_method=self._async_update_data,
        )
        self.websession = async_get_clientsession(hass)
        self.energy_company = self.config_entry.unique_id
        self.ontario_holidays = holidays.Canada(prov="ON", observed=True)

    @Throttle(REFRESH_RATES_INTERVAL)
    async def _async_update_data(self) -> None:
        """Parses the official XML document extracting the rates for
        the selected energy company.
        """
        async with async_timeout.timeout(self._timeout):
            response = await self.websession.get(RATES_URL)

        content = await response.text()
        tree = ET.fromstring(content)

        for company in tree.findall("GasBillData"):
            current_company = "{company_name}".format(
                company_name=company.find("Dist").text,
            )
            if current_company == self.energy_company:
                self.monthly_charge = float(company.find(XML_KEY_MONTHLY_CHARGE).text)
                self.gas_supply_charge = float(company.find(XML_KEY_GAS_SUPPLY_CHARGE).text)
                self.gas_supply_charge_price_adjustment = float(company.find(XML_KEY_GAS_SUPPLY_CHARGE_PRICE_ADJUSTMENT).text)
                self.transportation_charge_price_adjustment = float(company.find(XML_KEY_TRANSPORTATION_CHARGE_PRICE_ADJUSTMENT).text)
                self.delivery_charge_price_adjustment = float(company.find(XML_KEY_DELIVERY_CHARGE_PRICE_ADJUSTMENT).text)
                self.facility_carbon_charge = float(company.find(XML_KEY_FACILITY_CARBON_CHARGE).text)
                self.federal_carbon_charge = float(company.find(XML_KEY_FEDERAL_CARBON_CHARGE).text)
                self.transportation_charge = float(company.find(XML_KEY_TRANSPORTATION_CHARGE).text)
                self.gst = float(company.find(XML_KEY_GST).text)
                return

        self.logger.error("Could not find energy rates for %s", self.energy_company)
