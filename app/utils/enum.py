import enum


class Strategy(enum.Enum):
    TimeWorks = 1
    MaximumPowerConsumption = 2
    PeakEnergyConsumption = 3
    EnergyEfficiency = 4
    PercentageOfNetworkLoad = 5
    DurationOfOperatingTimeAtHighPower = 6
    AverageEnergyConsumptionPerHour = 7
