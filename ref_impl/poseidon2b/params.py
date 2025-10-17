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
        assert self.gf_degree == 32 and (self.state_len == 16 or self.state_len == 24)

        GF = gf.GF(2**self.gf_degree)

        x = GF.primitive_element
        ones = GF.Ones((self.state_len, self.state_len)) - GF.Identity(self.state_len)

        if self.state_len == 16:
            diagonal = GF(
                np.diag(
                    [
                        x**10,
                        x**3,
                        x**8,
                        x**11,
                        x**14,
                        GF(1),
                        x**15,
                        x**10 + GF(1),
                        x**4,
                        x**2 + GF(1),
                        x**6,
                        x**7,
                        x**13 + GF(1),
                        x**2,
                        x**5,
                        x + GF(1),
                    ]
                )
            )
            return ones + diagonal
        else:
            diagonal = GF(
                np.diag(
                    [
                        x**11 + x**7 + GF(1),
                        x**14 + x**5,
                        x**15 + x**8,
                        x**15 + x**5,
                        x**12 + x**3,
                        x**14 + x**3,
                        x**10 + x,
                        x**8 + x**3,
                        x**14 + GF(1),
                        x**5 + GF(1),
                        x**12 + x**4,
                        x**5 + x**4,
                        x**12 + x**11,
                        x**6 + x**3,
                        x**12 + x**5,
                        x**9 + x**3,
                        x**8 + x**5,
                        x**15 + x**10,
                        x**11 + x**7,
                        x + GF(1),
                        x**13 + x,
                        x**7 + x**5,
                        x**12 + x**2,
                        x**15 + x**9,
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


Poseidon2b_n32t16 = Poseidon2bPermutationParameters(32, 16, 8, 15, 7)
Poseidon2b_n32t24 = Poseidon2bPermutationParameters(32, 24, 8, 15, 7)

if __name__ == "__main__":
    print("This is not an executable module.")
    exit(1)
