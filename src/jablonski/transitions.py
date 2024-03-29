"""
    jablonski.transitions
    ~~~~~~~~~~~~~~~~~~~~~

    Abstraction for transitions.


    :copyright: 2024 by redpipy Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""


import pint
from poincare import Parameter, System, assign
from typing_extensions import dataclass_transform

from jablonski.states import State, initial


@dataclass_transform(field_specifiers=(initial,))
class EnergyTransferUpconversion(System):
    sensitizer: State = initial(0.0, default=0)
    activator: State = initial(0.0, default=0)
    relaxator: State = initial(0.0, default=0)

    rate: Parameter = assign(default=0)

    val = rate * sensitizer**2

    sensitization = sensitizer.derive() << -2 * val
    activation = activator.derive() << val
    relaxation = relaxator.derive() << val


@dataclass_transform(field_specifiers=(initial,))
class FluorescenceTransition(System):
    ground: State = initial(0.0, default=0)
    excited: State = initial(0.0, default=0)

    rate: Parameter = assign(default=0)

    val = rate * excited

    down = ground.derive() << val
    up = excited.derive() << -val

    @property
    def energy_difference(self) -> pint.Quantity:
        return self.excited.energy - self.ground.energy


@dataclass_transform(field_specifiers=(initial,))
class StateAbsorption(System):
    ground: State = initial(0.0, default=0)
    excited: State = initial(0.0, default=0)

    rate: Parameter = assign(default=0)

    val = rate * ground

    down = ground.derive() << -val
    up = excited.derive() << val

    @property
    def energy_difference(self) -> pint.Quantity:
        return self.excited.energy - self.ground.energy
