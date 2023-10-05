import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN ,
    CONF_WALLETS,
    CONF_CURRENCY,
    CONF_UPDATE_INTERVAL,
    DEFAULT_CONF_UPDATE_INTERVAL,
) 

COINGECKO_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_WALLETS): vol.All(cv.ensure_list, [cv.string]),
        vol.Required(CONF_CURRENCY): cv.string,
        vol.Optional(
            CONF_UPDATE_INTERVAL, default=DEFAULT_CONF_UPDATE_INTERVAL
        ): cv.string,

    }
)

COINGECKO_SCHEMA = vol.Schema(
    { 
        vol.Required(CONF_WALLETS): cv.string,
        vol.Required(CONF_CURRENCY): cv.string,
        vol.Optional(
            CONF_UPDATE_INTERVAL, default=DEFAULT_CONF_UPDATE_INTERVAL
        ): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {vol.Optional(DOMAIN): COINGECKO_SCHEMA}, extra=vol.ALLOW_EXTRA
)



class CoinGeckoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, info):
        errors: dict[str, str] = {}
        if info is not None:
            pass  # TODO: process info

        return self.async_show_form(
            step_id="user", data_schema=COINGECKO_SCHEMA , errors=errors,
        )