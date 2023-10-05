
import voluptuous as vol 
from homeassistant.core import HomeAssistant 
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType  
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
from datetime import timedelta

from pycoingecko import CoinGeckoAPI 

from .const import (
    DOMAIN ,
    CONF_WALLETS,
    CONF_CURRENCY, 
    DEFAULT_CONF_UPDATE_INTERVAL,
) 
PLATFORMS = ["sensor"]


import logging
_LOGGER = logging.getLogger(__name__)

COINGECKO_SCHEMA = vol.All(
    vol.Schema(
        {
            vol.Required(CONF_WALLETS): vol.All(cv.ensure_list, [cv.string]),
            vol.Required(CONF_CURRENCY): cv.string,
        },
        extra=vol.PREVENT_EXTRA,
    )
)
#cv.time_period
CONFIG_SCHEMA = vol.Schema(
    {vol.Optional(DOMAIN): COINGECKO_SCHEMA}, extra=vol.ALLOW_EXTRA
)


async def async_setup(hass: HomeAssistant, yaml_config: ConfigType) -> bool:
    """Activate Rhasspy Actions component."""
    _LOGGER.debug("async_setup ...")

    if DOMAIN not in yaml_config:
        _LOGGER.warn("not DOMAIN in configuration.yaml")
        return True

    config = yaml_config[DOMAIN]
    _LOGGER.debug(f'Config : {config}  ')   

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["coins"] = []
    hass.data[DOMAIN]["config"] = config 

    async def async_update_data():
        _LOGGER.debug("async_update_data ...") 
        _LOGGER.debug(f'hass.data[DOMAIN][coins] : {hass.data[DOMAIN]["coins"]}  ') 
        if DOMAIN in hass.data:
            listCoins = [coin.coin_id for coin in hass.data[DOMAIN]["coins"]]
            _LOGGER.debug(f'listCoins : {listCoins}  ') 
            if  len(listCoins)>0:
                return await hass.async_add_executor_job(run_coingecko, hass, listCoins, config[CONF_CURRENCY])

        return []

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name=DOMAIN,
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(minutes=DEFAULT_CONF_UPDATE_INTERVAL),
    )
    #await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN]["coordinator"] = coordinator

    _LOGGER.debug("async_setup END")
    return True


def run_coingecko(hass: HomeAssistant, listCoins:str, currency:str):
    _LOGGER.debug("run_coingecko ...") 
    
    cg = CoinGeckoAPI()
    coins = cg.get_coins_markets(ids=listCoins, vs_currency=currency)

    return coins
 