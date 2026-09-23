"""Compositional partition used in this exercise.

Simplified from the disorder-promoting / order-promoting split described in the
IDP literature (Uversky- and Dunker-style compositional analyses). Provided as a
fixed input to the exercise: participants are NOT asked to derive or modify it.

This file holds the partition and nothing else. Which characters an input
sequence may contain is a requirements decision, not given material.

NOTE: this is a teaching simplification, not a validated predictor.
"""

DISORDER_PROMOTING = frozenset("PESQKAGRDT")
ORDER_PROMOTING = frozenset("WCFIYVLMNH")
