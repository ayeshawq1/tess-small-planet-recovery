
"""
ADAPT-v1
Frozen Week 14 adaptive preprocessing rule.

This function uses only measured host variability.
It does not use injected planet truth.
"""

ADAPT_V1_RMS_THRESHOLD = 0.000215


def adapt_v1_choose_method(robust_rms):
    robust_rms = float(robust_rms)

    if robust_rms <= ADAPT_V1_RMS_THRESHOLD:
        return "BASELINE"

    return "SG_501"
