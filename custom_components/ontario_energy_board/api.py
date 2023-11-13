"""Utility methods used by the Ontario Energy Board integration.

TECH-DEBT: This class is not being in use anymore. At the moment it's only being
used for unit tests. These tests should instead be against the sensor component itself.
"""
import aiohttp
import async_timeout
import logging
import xml.etree.ElementTree as ET
from datetime import date
from typing import Final

import holidays
from homeassistant.util.dt import as_local, now

from .const import (
    RATES_URL,

)


_LOGGER: Final = logging.getLogger(__name__)


async def get_energy_companies() -> list[str]:
    """Generates a list of all energy companies available
    in the XML document including the available classes.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(RATES_URL) as response:
            content = await response.text()

    tree = ET.fromstring(content)

    all_companies = [
        "{company_name}".format(
            company_name=company.find("Dist").text,
        )
        for company in tree.findall("GasBillData")
    ]
    all_companies.sort()

    return all_companies


class OntarioEnergyBoard:
    """Class to communication with the Ontario Energy Rate services."""

    _timeout = 10
    off_peak_rate = None
    mid_peak_rate = None
    on_peak_rate = None

    def __init__(self, energy_company, websession):
        self.energy_company = energy_company
        self.websession = websession
        self.ontario_holidays = holidays.Canada(prov="ON", observed=True)

    async def get_rates(self):
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
                self.off_peak_rate = float(company.find(XML_KEY_OFF_PEAK_RATE).text)
                self.mid_peak_rate = float(company.find(XML_KEY_MID_PEAK_RATE).text)
                self.on_peak_rate = float(company.find(XML_KEY_ON_PEAK_RATE).text)
                return

        _LOGGER.error("Could not find energy rates for %s", self.energy_company)




