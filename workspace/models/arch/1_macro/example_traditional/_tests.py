import sys
import os

# fmt: off
THIS_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MACRO_NAME = os.path.basename(THIS_SCRIPT_DIR)
sys.path.append(os.path.abspath(os.path.join(THIS_SCRIPT_DIR, '..', '..', '..', '..')))
from scripts import utils as utl
import scripts
import math
# fmt: on

def unique_power_of_two_pairs(num, sym):
    """
    Generator that yields unique pairs (a, b) of powers of 2 such that:
    a * b == 2**n
    and a <= b (to avoid duplicates like (8,2) when (2,8) is already counted)
    """
    n = int(math.log2(num))
    target = 2 ** n
    for i in range(n + 1):  # i is the exponent for a
        j = n - i           # j is the exponent for b so that a*b = 2^n
        a, b = 2 ** i, 2 ** j
        if a <= b or sym:
            yield (a, b)

def test_area_energy_breakdown():
    """
    ### Area and energy breakdown
    This example architecture doesn't have a suite of tests, but you may
    look at the other example architectures for inspiration.        
    """
    results = utl.single_test(utl.quick_run(macro=MACRO_NAME))

    results = utl.parallel_test(
        utl.delayed(utl.quick_run)(
            macro=MACRO_NAME,
            variables=dict(
                VOLTAGE=v,
            ),
        )
        for v in [.67]
        # for v in [0.5, .6, .8, .9, 1]
    )
    results.combine_per_component_energy(
        ["A_Buffer", "mac_weight_register"], "A_Buffer"
    )
    results.clear_zero_areas()
    results.clear_zero_energies()
    return results

def test_system_config(PEs: int):
    """
    ### Area and energy breakdown
    This example architecture doesn't have a suite of tests, but you may
    look at the other example architectures for inspiration.        
    """
    results = utl.single_test(utl.quick_run(macro=MACRO_NAME))

    results = utl.parallel_test(
        utl.delayed(utl.quick_run)(
            macro=MACRO_NAME,
            variables=dict(
                PE_MESH_X=config[0],
                PE_MESH_Y=config[1],
            ),
        )
        for config in unique_power_of_two_pairs(PEs, True)
        # for v in [0.5, .6, .8, .9, 1]
    )
    results.combine_per_component_energy(
        ["A_Buffer", "mac_weight_register"], "A_Buffer"
    )
    results.clear_zero_areas()
    results.clear_zero_energies()
    return results

def test_global_pe_size(config: tuple):
    """
    ### Area and energy breakdown
    This example architecture doesn't have a suite of tests, but you may
    look at the other example architectures for inspiration.        
    """
    results = utl.single_test(utl.quick_run(macro=MACRO_NAME))

    results = utl.parallel_test(
        utl.delayed(utl.quick_run)(
            macro=MACRO_NAME,
            variables=dict(
                PE_MESH_X=config[0],
                PE_MESH_Y=config[1],
                GLOBAL_PE_SIZE=elem,
            ),
        )
        for elem in [2**sz for sz in range(12, 25, 2)]
        # for v in [0.5, .6, .8, .9, 1]
    )
    results.combine_per_component_energy(
        ["A_Buffer", "mac_weight_register"], "A_Buffer"
    )
    results.clear_zero_areas()
    results.clear_zero_energies()
    return results

if __name__ == "__main__":
    test_area_energy_breakdown()