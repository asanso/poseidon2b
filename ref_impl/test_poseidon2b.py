from .poseidon2b import Poseidon2b_n32t16, Poseidon2b_n32t24
import galois as gf


def test_Poseidon2b_n32t16_against_known_answer_test():
    """
    Test vector taken from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.ipynb.
    """
    pos2b = Poseidon2b_n32t16

    INIT_STATE = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    EXPECTED_STATE = [
        3263689815,
        3510016260,
        531948390,
        201633991,
        2369968409,
        2911726907,
        3767115820,
        1283168574,
        3383130628,
        115255156,
        1084253133,
        337390485,
        2474582269,
        1077148670,
        1561443687,
        3531824307,
    ]

    GF = gf.GF(2**pos2b.gf_degree)

    init_state = GF(INIT_STATE)
    computed_state = pos2b.permute(init_state)

    assert all(computed_state == EXPECTED_STATE)


def test_Poseidon2b_n32t24_against_known_answer_test():
    """
    Test vector taken from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.ipynb.
    """
    pos2b = Poseidon2b_n32t24

    INIT_STATE = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
    ]
    EXPECTED_STATE = [
        629457651,
        3133113043,
        1957366598,
        540552150,
        2700255999,
        952649519,
        1287886501,
        2162448165,
        4149492888,
        1405122613,
        4290387076,
        1297542638,
        3948678925,
        2832483533,
        1878944148,
        2634845448,
        1330014154,
        1206884896,
        2974561210,
        4183012554,
        1858102117,
        1471257888,
        639738976,
        2618256400,
    ]

    GF = gf.GF(2**pos2b.gf_degree)

    init_state = GF(INIT_STATE)
    computed_state = pos2b.permute(init_state)

    assert all(computed_state == EXPECTED_STATE)
