"""
Poseidon2b test vectors are taken from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.ipynb.
"""

from .poseidon2b import (
    Poseidon2b_n32t16,
    Poseidon2b_n32t24,
    Poseidon2b,
    Poseidon2b_n64t8,
    Poseidon2b_n128t4,
    Poseidon2b_n128t6,
)


def test_Poseidon2b_n32t16_against_known_answer_test():
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

    GF = pos2b.galois_field()

    init_state = GF(INIT_STATE)
    computed_state = Poseidon2b(pos2b).permute(init_state)

    assert list(map(lambda x: int(x), computed_state)) == EXPECTED_STATE


def test_Poseidon2b_n32t24_against_known_answer_test():
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

    GF = pos2b.galois_field()

    init_state = GF(INIT_STATE)
    computed_state = Poseidon2b(pos2b).permute(init_state)

    assert list(map(lambda x: int(x), computed_state)) == EXPECTED_STATE


def test_Poseidon2b_n64t8_against_known_answer_test():
    pos2b = Poseidon2b_n64t8

    INIT_STATE = [0, 1, 2, 3, 4, 5, 6, 7]
    EXPECTED_STATE = [
        5630310687624063658,
        6289737725441534884,
        14084478720876142317,
        2253230934601515370,
        7483738063588220639,
        3747464340416986385,
        7031526246119211789,
        17484719721536023833,
    ]

    GF = pos2b.galois_field()

    init_state = GF(INIT_STATE)
    computed_state = Poseidon2b(pos2b).permute(init_state)

    assert list(map(lambda x: int(x), computed_state)) == EXPECTED_STATE


def test_Poseidon2b_n128t4_against_known_answer_test():
    pos2b = Poseidon2b_n128t4

    INIT_STATE = [0, 1, 2, 3]
    EXPECTED_STATE = [
        190694032047300303914125217899381430126,
        5112655656068718841781059291681792676,
        313609626244364533523501173704655550348,
        37684179678214226142224368748917426745,
    ]

    GF = pos2b.galois_field()

    init_state = GF(INIT_STATE)
    computed_state = Poseidon2b(pos2b).permute(init_state)

    assert list(map(lambda x: int(x), computed_state)) == EXPECTED_STATE


def test_Poseidon2b_n128t6_against_known_answer_test():
    pos2b = Poseidon2b_n128t6

    INIT_STATE = [0, 1, 2, 3, 4, 5]
    EXPECTED_STATE = [
        210105174278901385894543708583193164885,
        228518741170243896768842647243322832405,
        45838152944830247173621358189720241591,
        332050717679287485158248364790277533378,
        179338549228488138204138874001126554601,
        280548768647529633273240681102980736256,
    ]

    GF = pos2b.galois_field()

    init_state = GF(INIT_STATE)
    computed_state = Poseidon2b(pos2b).permute(init_state)

    assert list(map(lambda x: int(x), computed_state)) == EXPECTED_STATE
