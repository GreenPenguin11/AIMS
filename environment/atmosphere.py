import math
from dataclasses import dataclass


@dataclass
class AtmosphereState:

    altitude: float       # m
    temperature: float    # K
    pressure: float       # Pa
    density: float        # kg/m^3
    speed_of_sound: float # m/s
    dynamic_viscosity: float  # Pa*s


class StandardAtmosphere:

    # Constants
    G = 9.80665           # m/s^2
    R = 287.05287         # J/(kg*K)
    GAMMA = 1.4

    # Sea-level conditions
    T0 = 288.15           # K
    P0 = 101325.0         # Pa

    # Lapse rate
    LAPSE_RATE = -0.0065  # K/m

    # Tropopause
    H_TROPOPAUSE = 11000.0  # m

    def evaluate(self, altitude: float) -> AtmosphereState:

        if altitude < 0:
            raise ValueError("Altitude cannot be negative.")

        if altitude > 20000:
            raise ValueError(
                "Current atmosphere model only supports 0-20,000 m."
            )

        if altitude <= self.H_TROPOPAUSE:
            temperature = (
                self.T0 + self.LAPSE_RATE * altitude
            )

            pressure = self.P0 * (
                temperature / self.T0
            ) ** (
                -self.G / (self.LAPSE_RATE * self.R)
            )

        else:
            t11 = (
                self.T0
                + self.LAPSE_RATE * self.H_TROPOPAUSE
            )

            p11 = self.P0 * (
                t11 / self.T0
            ) ** (
                -self.G / (self.LAPSE_RATE * self.R)
            )


            temperature = t11

            pressure = p11 * math.exp(
                -self.G
                * (altitude - self.H_TROPOPAUSE)
                / (self.R * temperature)
            )

        density = pressure / (self.R * temperature)

        speed_of_sound = math.sqrt(
            self.GAMMA * self.R * temperature
        )

        # Instert Viscosity Here when done
        dynamic_viscosity=999

        return AtmosphereState(
            altitude=altitude,
            temperature=temperature,
            pressure=pressure,
            density=density,
            speed_of_sound=speed_of_sound,
            dynamic_viscosity=dynamic_viscosity,
        )
