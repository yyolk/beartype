#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2020 Cecil Curry.
# See "LICENSE" for further details.

'''
**Beartype decorator general-purpose code snippets.**

This private submodule *only* defines **code snippets** (i.e., triple-quoted
pure-Python code constants formatted and concatenated together into wrapper
functions implementing type-checking for decorated callables).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ CONSTANTS ~ param                 }....................
PARAM_NAME_FUNC = '__beartype_func'
'''
Name of the **private decorated callable parameter** (i.e.,
:mod:`beartype`-specific parameter whose default value is the decorated
callable implicitly passed to all wrapper functions generated by the
:func:`beartype.beartype` decorator).
'''


PARAM_NAME_TYPISTRY = '__beartypistry'
'''
Name of the **private beartypistry parameter** (i.e., :mod:`beartype`-specific
parameter whose default value is the beartypistry singleton implicitly passed
to all wrapper functions generated by the :func:`beartype.beartype` decorator).
'''

# ....................{ CODE                              }....................
CODE_SIGNATURE = f'''def {{func_wrapper_name}}(
    *args,
    {PARAM_NAME_FUNC}={PARAM_NAME_FUNC},
    {PARAM_NAME_TYPISTRY}={PARAM_NAME_TYPISTRY},
    **kwargs
):'''
'''
PEP-agnostic code snippet declaring the signature of the wrapper function
type-checking the decorated callable.
'''

# ....................{ CODE ~ init                       }....................
CODE_INIT_PARAMS_POSITIONAL_LEN = '''
    # Localize the number of passed positional arguments for efficiency.
    __beartype_args_len = len(args)'''
'''
PEP-agnostic code snippet localizing the number of passed positional arguments
for callables accepting one or more such arguments.
'''


#FIXME: Note that NumPy provides an efficient means of generating a large
#number of pseudo-random integers all-at-once. The core issue there, of
#course, is that we then need to optionally depend upon and detect NumPy,
#which then requires us to split our random integer generation logic into two
#parallel code paths that we'll then have to maintain -- and the two will be
#rather different. In any case, here's how one generates a NumPy array
#containing 100 pseudo-random integers in the range [0, 127]:
#    random_ints = numpy.random.randint(128, size=100)
#To leverage that sanely, we'd need to:
#* Globally cache that array somewhere.
#* Globally cache the current index into that array.
#* When NumPy is unimportable, fallback to generating a Python list containing
#  the same number of pseudo-random integers in the same range.
#* In either case, we'd probably want to wrap that logic in a globally
#  accessible infinite generator singleton that returns another pseudo-random
#  integer every time you iterate it. This assumes, of course, that iterating
#  generators is reasonably fast in Python. (If not, just make that a getter
#  method of a standard singleton object.)
#* Replace the code snippet below with something resembling:
#      '''
#      __beartype_random_int = next(__beartype_random_int_generator)
#      '''
#Note that thread concurrency issues are probable ignorable here, but that
#there's still a great deal of maintenance and refactoring that would need to
#happen to sanely support this. In other words, ain't happenin' anytime soon.

CODE_INIT_RANDOM_INT = '''
    # Generate and localize a sufficiently large pseudo-random integer for
    # subsequent indexation in type-checking randomly selected container items.
    __beartype_random_int = __beartype_getrandbits(32)'''
'''
PEP-specific code snippet generating and localizing a pseudo-random integer for
subsequent reference when type-checking randomly selected container items.

This integer is guaranteed to be in the range of **standard non-big integers**
(i.e., representable as type :class:`int`  rather :class:`BigNum`), which is
to say 0–``2**32 - 1``. Since the cost of generating integers to this maximum
bit length is *approximately* the same as generating integers of much smaller
bit lengths, this maximum is preferred. Although big integers transparently
support the same operations as non-big integers, the latter are dramatically
more efficient with respect to both space and time consumption and thus
preferred. Lastly, standard integers are portably representable in C with at
least 32 but *not* necessarily more bits across all sane architectures.

Usage
-----
Since *most* containers are likely to contain substantially fewer items than
the maximum integer in this range, pseudo-random container indices are
efficiently selectable by simply taking the modulo of this local variable with
the lengths of those containers.

Any container containing more than this maximum number of items is typically
defined as a disk-backed data structure (e.g., Pandas dataframe) rather than an
in-memory standard object (e.g., :class:`list`). Since :mod:`beartype`
currently ignores the former with respect to deep type-checking, this local
typically suffices for real-world in-memory containers. For edge-case
containers containing more than this maximum number of items, :mod:`beartype`
will only deeply type-check items with indices in this range; all trailing
items will *not* be deeply type-checked, which we consider an acceptable
tradeoff, given the infeasibility of even storing such objects in memory.

Caveats
-------
**The only safely callable function declared by the stdlib** :mod:`random`
**module is** :func:`random.getrandbits`. While that function is efficiently
implemented in C, all other functions declared by that module are inefficiently
implemented in Python. In fact, their implementations are sufficiently
inefficient that there exist numerous online articles lamenting the fact.

See Also
--------
https://gist.github.com/terrdavis/1b23b7ff8023f55f627199b09cfa6b24#gistcomment-3237209
    Self GitHub comment introducing the core concepts embodied by this snippet.
https://eli.thegreenplace.net/2018/slow-and-fast-methods-for-generating-random-integers-in-python
    Authoritative article profiling various :mod:`random` callables.
'''

# ....................{ CODE ~ return                     }....................
CODE_RETURN_UNCHECKED = f'''
    # Call this function with all passed parameters and return the value
    # returned from this call.
    return {PARAM_NAME_FUNC}(*args, **kwargs)'''
'''
PEP-agnostic code snippet calling the decorated callable *without*
type-checking the value returned by that call (if any).
'''

# ....................{ CODE ~ indent                     }....................
CODE_INDENT_1 = '    '
'''
PEP-agnostic code snippet expanding to a single level of indentation.
'''


CODE_INDENT_2 = CODE_INDENT_1*2
'''
PEP-agnostic code snippet expanding to two levels of indentation.
'''


CODE_INDENT_3 = CODE_INDENT_2 + CODE_INDENT_1
'''
PEP-agnostic code snippet expanding to three levels of indentation.
'''
