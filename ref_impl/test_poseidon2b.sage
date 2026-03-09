# ref_impl/poseidon2b/test_poseidon2b.sage
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
# add the parent so the package "poseidon2b" is importable
sys.path.insert(0, str(HERE.parent))

from poseidon2b.params import Poseidon2b_n32t16
from poseidon2b.poseidon2b import Poseidon2b

def main():
    pos2b = Poseidon2b_n32t16
    INIT_STATE = list(range(16))
    EXPECTED_STATE = [
        3263689815, 3510016260, 531948390, 201633991,
        2369968409, 2911726907, 3767115820, 1283168574,
        3383130628, 115255156, 1084253133, 337390485,
        2474582269, 1077148670, 1561443687, 3531824307,
    ]
    GF = pos2b.galois_field()
    init_state = GF(INIT_STATE)
    computed_state = Poseidon2b(pos2b).permute(init_state)
    as_ints = list(map(int, computed_state))
    print("Computed:", as_ints)
    assert as_ints == EXPECTED_STATE, "KAT failed"
    print("OK")

if __name__ == "__main__":
    main()
