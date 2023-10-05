from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import ATTR_ATTRIBUTION

from .const import (
    DOMAIN,
    CONF_COIN_ID,
    CONF_WALLETS, 
    CONF_VOLUME,
    CONF_PRICE,
    CONF_NAME
)

import logging
_LOGGER = logging.getLogger(__name__)

class CoinSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Coinbase.com sensor."""

    def __init__(self, coordinator, data):
        """Initialize the sensor."""
        super().__init__(coordinator)
        _LOGGER.debug(f'ATTR_ATTRIBUTION ${ATTR_ATTRIBUTION} ') 
        self._coin_id = data[CONF_COIN_ID]
        if CONF_NAME in data:
            self._name = data[CONF_NAME]
        else:
            self._name = self.coin_id
        self._wallet = data[CONF_WALLETS]
        #self._volume = data[CONF_VOLUME]
        #self._price = data[CONF_PRICE]
        self._attr_extra_state_attributes = {}

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def coin_id(self):
        """Return the coind_id of the sensor."""
        return self._coin_id

    @property
    def wallet(self):
        """Return the wallet of the sensor."""
        return self._wallet

    @property
    def native_value(self): 
        _LOGGER.debug(f'native_value ... ') 
        _LOGGER.debug(f'self.name ${self.name} ')  
        _LOGGER.debug(f'self.wallet ${self.wallet} ')  
        """Return the state of the sensor.""" 
        if self.coordinator.data != None:
            _LOGGER.debug(f'self.coordinator.data : {self.coordinator.data}  ') 
            coin = [coin for coin in self.coordinator.data if coin['id'] == self.coin_id][0]
            
            self._attr_extra_state_attributes['market_cap'] = coin['market_cap']
            self._attr_extra_state_attributes['market_cap_rank'] = coin['market_cap_rank']
            self._attr_extra_state_attributes['fully_diluted_valuation'] = coin['fully_diluted_valuation']
            self._attr_extra_state_attributes['total_volume'] = coin['total_volume']
            self._attr_extra_state_attributes['high_24h'] = coin['high_24h']
            self._attr_extra_state_attributes['low_24h'] = coin['low_24h']
            self._attr_extra_state_attributes['price_change_percentage_24h'] = coin['price_change_percentage_24h']
            self._attr_extra_state_attributes['market_cap_change_percentage_24h'] = coin['market_cap_change_percentage_24h']
            self._attr_extra_state_attributes['circulating_supply'] = coin['circulating_supply']
            self._attr_extra_state_attributes['ath'] = coin['ath']
            self._attr_extra_state_attributes['ath_change_percentage'] = coin['ath_change_percentage']

            #self._attr_extra_state_attributes['profit'] = (self._volume*coin['current_price']) - (self._volume*self._price)
            #self._attr_extra_state_attributes['profit_percentage'] = self._attr_extra_state_attributes['profit'] / (self._volume*self._price)
            
            return coin['current_price']
        return False