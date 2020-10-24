#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright 2014-2020 by Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype** `PEP 544`_**-compliant type hint test data.**

.. _PEP 544:
    https://www.python.org/dev/peps/pep-0544
'''

# ....................{ TODO                              }....................
#FIXME: Test user-defined multiple-inherited protocols (i.e., user-defined
#classes directly subclassing the "typing.Protocol" ABC and one or more other
#superclasses) once @beartype supports these protocols as well.

# ....................{ IMPORTS                           }....................
from abc import abstractmethod
from beartype._util.py.utilpyversion import IS_PYTHON_AT_LEAST_3_8
from beartype_test.unit.data.hint.pep.data_hintpepmeta import (
    PepHintClassedMetadata,
    PepHintPithUnsatisfiedMetadata,
)

# ....................{ ADDERS                            }....................
def add_data(data_module: 'ModuleType') -> None:
    '''
    Add `PEP 544`_**-compliant type hint test data to various global containers
    declared by the passed module.

    Parameters
    ----------
    data_module : ModuleType
        Module to be added to.

    .. _PEP 544:
        https://www.python.org/dev/peps/pep-0544
    '''

    # If the active Python interpreter targets less than Python < 3.8, this
    # interpreter fails to support PEP 544. In this case, reduce to a noop.
    if not IS_PYTHON_AT_LEAST_3_8:
        return
    # Else, the active Python interpreter targets at least Python >= 3.8 and
    # thus supports PEP 544.

    # Defer Python >= 3.8-specific imports.
    from typing import Protocol, SupportsInt, runtime_checkable

    # User-defined protocol declaring arbitrary concrete and abstract methods.
    @runtime_checkable
    class ProtocolCustom(Protocol):
        def alpha(self) -> str:
            return 'Of a Spicily sated'

        @abstractmethod
        def omega(self) -> str: pass

    # User-defined class structurally (i.e., implicitly) satisfying *WITHOUT*
    # explicitly subclassing this user-defined protocol.
    class ProtocolCustomStructural(object):
        def alpha(self) -> str:
            return "Sufferance's humus excursion, humility’s endurance, an"

        def omega(self) -> str:
            return 'Surfeit need'

    # User-defined class structurally (i.e., implicitly) satisfying *WITHOUT*
    # explicitly subclassing the predefined "typing.SupportsInt" protocol.
    class SupportsIntStructural(object):
        def __int__(self) -> int:
            return 42

    # Add PEP 544-specific test type hints to this dictionary global.
    data_module.HINT_PEP_TO_META.update({
        # ................{ PROTOCOLS                         }................
        # Despite appearances, protocols implicitly subclass "typing.Generic"
        # and thus do *NOT* transparently reduce to standard types.

        # Predefined "typing" protocol.
        SupportsInt: PepHintClassedMetadata(
            pep_sign=Protocol,
            is_pep484_user=True,
            piths_satisfied=(
                # Structurally subtyped instance.
                SupportsIntStructural(),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata('For durance needs.'),
            ),
        ),

        # User-defined protocol.
        ProtocolCustom: PepHintClassedMetadata(
            pep_sign=Protocol,
            is_pep484_user=True,
            piths_satisfied=(
                # Structurally subtyped instance.
                ProtocolCustomStructural(),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata('For durance needs.'),
            ),
        ),
    })