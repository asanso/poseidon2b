from dataclasses import dataclass
import galois as gf
import numpy as np
from .utils import SHAKEUtils


@dataclass
class Poseidon2bPermutationParameters:
    gf_degree: int
    state_len: int
    num_full_rounds: int
    num_partial_rounds: int
    alpha: int

    def num_total_rounds(self) -> int:
        return self.num_full_rounds + self.num_partial_rounds

    def num_initial_full_rounds(self) -> int:
        return self.num_full_rounds // 2

    def num_final_full_rounds(self) -> int:
        return self.num_full_rounds - self.num_initial_full_rounds()

    def generate_partial_round_matrix(self) -> gf.FieldArray:
        assert self.gf_degree == 32 and self.state_len == 16

        GF = gf.GF(2**self.gf_degree)

        prim_elem = GF.primitive_element
        ones = GF.Ones((self.state_len, self.state_len)) - GF.Identity(self.state_len)
        diagonal = GF(
            np.diag(
                [
                    prim_elem**10,
                    prim_elem**3,
                    prim_elem**8,
                    prim_elem**11,
                    prim_elem**14,
                    GF(1),
                    prim_elem**15,
                    prim_elem**10 + GF(1),
                    prim_elem**4,
                    prim_elem**2 + GF(1),
                    prim_elem**6,
                    prim_elem**7,
                    prim_elem**13 + GF(1),
                    prim_elem**2,
                    prim_elem**5,
                    prim_elem + GF(1),
                ]
            )
        )

        return ones + diagonal

    def generate_full_round_matrix(self) -> gf.FieldArray:
        assert self.state_len != 4 and self.state_len != 6

        GF = gf.GF(2**self.gf_degree)

        prim_elem = GF.primitive_element
        mat4x4 = GF(
            [
                [
                    prim_elem**2 + GF(1),
                    prim_elem**2 + prim_elem + GF(1),
                    1,
                    prim_elem + GF(1),
                ],
                [prim_elem**2, prim_elem**2 + prim_elem, 1, 1],
                [
                    1,
                    prim_elem + GF(1),
                    prim_elem**2 + GF(1),
                    prim_elem**2 + prim_elem + GF(1),
                ],
                [1, 1, prim_elem**2, prim_elem**2 + prim_elem],
            ]
        )

        tby4 = self.state_len // 4
        blocks = [
            [prim_elem * mat4x4 if i == j else mat4x4 for j in range(tby4)]
            for i in range(tby4)
        ]

        return GF(np.block(blocks))

    def is_full_round(self, ridx: int) -> bool:
        return (ridx < self.num_total_rounds()) and (
            (ridx < self.num_initial_full_rounds())
            or (ridx >= (self.num_initial_full_rounds() + self.num_partial_rounds))
        )

    def generate_round_constants(self):
        shake_utils = SHAKEUtils(self.gf_degree)
        shake_reader = shake_utils.init_shake_reader()

        GF = gf.GF(2**self.gf_degree)

        rc_elems = [
            i
            for i in shake_utils.get_random_elements(
                self.num_total_rounds() * self.state_len, shake_reader
            )
        ]
        rc_mat = GF(rc_elems).reshape((self.num_total_rounds(), self.state_len))

        for ridx in range(self.num_total_rounds()):
            if not self.is_full_round(ridx):
                for sidx in range(1, self.state_len):
                    rc_mat[ridx][sidx] = GF(0)

        return rc_mat

    def permute(self, state: gf.FieldArray) -> gf.FieldArray:
        assert len(state) == self.state_len

        ROUND_CONSTANTS = self.generate_round_constants()
        FULL_ROUND_MATRIX = self.generate_full_round_matrix()
        PARTIAL_ROUND_MATRIX = self.generate_partial_round_matrix()

        GF = gf.GF(2**self.gf_degree)

        def AddRoundCons(state: gf.FieldArray, ridx: int) -> gf.FieldArray:
            return state + ROUND_CONSTANTS[ridx]

        def SubWordsRF(state: gf.FieldArray) -> gf.FieldArray:
            return GF(list(map(lambda x: x**self.alpha, state)))

        def SubWordsRP(state: gf.FieldArray) -> gf.FieldArray:
            state[0] = state[0] ** self.alpha
            return state

        def RoundFull(state: gf.FieldArray, ridx: int) -> gf.FieldArray:
            state = AddRoundCons(state, ridx)
            state = SubWordsRF(state)
            state = np.matmul(FULL_ROUND_MATRIX, state)

            return state

        def RoundPartial(state: gf.FieldArray, ridx: int) -> gf.FieldArray:
            state = AddRoundCons(state, ridx)
            state = SubWordsRP(state)
            state = np.matmul(PARTIAL_ROUND_MATRIX, state)

            return state

        state = np.matmul(FULL_ROUND_MATRIX, state)

        for ridx in range(self.num_total_rounds()):
            if self.is_full_round(ridx):  # full rounds
                state = RoundFull(state, ridx)
            else:  # partial rounds
                state = RoundPartial(state, ridx)

        return state


Poseidon2b_n32t16 = Poseidon2bPermutationParameters(32, 16, 8, 15, 7)

if __name__ == "__main__":
    print("This is not an executable module.")
    exit(1)
