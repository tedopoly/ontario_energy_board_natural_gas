"""Constants for the Ontario Energy Board integration."""
from datetime import timedelta

DOMAIN = "ontario_energy_board_natural_gas"

CONF_ENERGY_COMPANY = "energy_company"

RATES_URL = "https://www.oeb.ca/_html/calculator/data/GasBillData.xml"

RATE_UNIT_OF_MEASURE = "CA$/kWh"

REFRESH_RATES_INTERVAL = timedelta(days=1)
SCAN_INTERVAL = timedelta(minutes=1)


XML_KEY_MONTHLY_CHARGE = "MC"
XML_KEY_GAS_SUPPLY_CHARGE = "CM"
XML_KEY_GAS_SUPPLY_CHARGE_PRICE_ADJUSTMENT = "CMPA"
XML_KEY_TRANSPORTATION_CHARGE_PRICE_ADJUSTMENT = "TCPA"
XML_KEY_DELIVERY_CHARGE_PRICE_ADJUSTMENT = "DCPA"

XML_KEY_FACILITY_CARBON_CHARGE = "FacCC"
XML_KEY_FEDERAL_CARBON_CHARGE = "FedCC"
XML_KEY_TRANSPORTATION_CHARGE = "TC"
XML_KEY_GST = "GST"


