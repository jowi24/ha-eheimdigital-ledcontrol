"""The EHEIM LEDcontrol+ light controller."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, override

from .classic_led_ctrl import EheimDigitalClassicLEDControl
from .device import EheimDigitalDevice
from .types import EheimDigitalDataMissingError

if TYPE_CHECKING:
    from .hub import EheimDigitalHub
    from .types import UsrDtaPacket


class EheimDigitalLEDControl(EheimDigitalClassicLEDControl):
    """Represent an EHEIM LEDcontrol+ light controller."""

    tankconfig: list[str]
    power: list[int]

    def __init__(self, hub: EheimDigitalHub, usrdta: UsrDtaPacket) -> None:
        """Initialize an LEDcontrol+ light controller."""
        EheimDigitalDevice.__init__(self, hub, usrdta)
        self.tankconfig = json.loads(usrdta["tankconfig"])
        self.power = json.loads(usrdta["power"])

    @property
    def number_of_channels(self) -> int:
        """Return the number of configured controller channels."""
        return len(self.tankconfig)

    @property
    @override
    def light_level(self) -> tuple[int | None, ...]:
        """Return the current light level of the channels."""
        if self.ccv is None:
            raise EheimDigitalDataMissingError
        return tuple(
            self.ccv["currentValues"][channel] if self.tankconfig[channel] else None
            for channel in range(self.number_of_channels)
        )

    @property
    @override
    def power_consumption(self) -> tuple[float | None, ...]:
        """Return the power consumption of the channels."""
        if self.ccv is None:
            raise EheimDigitalDataMissingError
        return tuple(
            self.power[channel] * self.ccv["currentValues"][channel]
            if self.tankconfig[channel]
            else None
            for channel in range(self.number_of_channels)
        )

    @override
    def as_dict(self) -> dict[str, Any]:
        """Return the device as a dictionary."""
        return {
            "tankconfig": self.tankconfig,
            "power": self.power,
            **super().as_dict(),
        }
