"""Support for currencylayer.com exchange rates service."""
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType


from .const import (
    DOMAIN,
    CONF_COIN_ID,
    CONF_WALLETS, 
    CONF_VOLUME,
    CONF_PRICE,
    CONF_NAME
)
from .CoinSensor import CoinSensor

import logging
_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_COIN_ID): cv.string, 
        vol.Required(CONF_WALLETS): cv.string, 
        vol.Optional(CONF_NAME): cv.string, 
        vol.Optional(CONF_VOLUME): vol.Coerce(float), 
        vol.Optional(CONF_PRICE): vol.Coerce(float), 
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Blockchain.com sensors."""   
    
    if DOMAIN not in hass.data:
        _LOGGER.warn("not DOMAIN in configuration.yaml")
        return True

    _LOGGER.debug("setup_platform ...")
#     _LOGGER.debug(f'hass.data[DOMAIN] : {hass.data[DOMAIN]}  ') 
    _LOGGER.debug(f'config : {config}  ') 

    coin = CoinSensor(hass.data[DOMAIN]["coordinator"], config) 
    add_entities(
        [coin], True
    )
    hass.data[DOMAIN]["coins"].append(coin)


    return True