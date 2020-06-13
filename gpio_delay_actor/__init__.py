# -*- coding: utf-8 -*-
import time

from modules import cbpi
from modules.core.hardware import ActorBase
from modules.core.props import Property

import RPi.GPIO as GPIO


@cbpi.actor
class GPIODelay(ActorBase):

    gpio = int(
        Property.Select("GPIO", options=range(28),
                        description="GPIO pin number")
    )
    delay = Property.Number(
        "Minimum delay",
        configurable=True,
        default_value=300,
        unit="s",
        description="Minimum wait time before switching on (s)",
    )

    switched_off_at = None

    def init(self):
        GPIO.setup(self.gpio, GPIO.OUT)
        GPIO.output(self.gpio, 0)

    def on(self, power=0):
        cbpi.app.logger.info("Request to switch on GPIO %d" % self.gpio)
        if GPIO.input(self.gpio) == 1:
            cbpi.app.logger.info("GPIO already on %d" % self.gpio)
            return

        if self.switched_off_at is not None:
            since_last_off = time.time() - self.switched_off_at
            cbpi.app.logger.info(
                "GPIO %d last switched off %d seconds ago" %
                (self.gpio, since_last_off)
            )

            if since_last_off < self.delay:
                cbpi.app.logger.info(
                    "Not enough time since last switched off GPIO %d" %
                    self.gpio
                )
                return

        cbpi.app.logger.info("Switching on GPIO %d" % self.gpio)
        GPIO.output(self.gpio, 1)

    def off(self):
        cbpi.app.logger.info("Request to switch off GPIO %d" % self.gpio)
        if GPIO.input(self.gpio) == 0:
            cbpi.app.logger.info("GPIO already off %d" % self.gpio)
            return

        cbpi.app.logger.info("Switching off GPIO %d" % self.gpio)
        self.switched_off_at = time.time()
        GPIO.output(self.gpio, 0)
