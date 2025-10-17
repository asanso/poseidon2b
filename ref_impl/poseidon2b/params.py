from dataclasses import dataclass
import galois as gf
import numpy as np
from scipy.linalg import circulant
from .utils import SHAKEUtils


@dataclass
class Poseidon2bParameters:
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

    def galois_field(self) -> type[gf.FieldArray]:
        if self.gf_degree == 128:
            return gf.GF(
                2**self.gf_degree, irreducible_poly="x^128 + x^7 + x^2 + x + 1"
            )
        else:
            return gf.GF(2**self.gf_degree)

    def generate_partial_round_matrix(self) -> gf.FieldArray:
        assert (
            (self.gf_degree == 32 and (self.state_len == 16 or self.state_len == 24))
            or (self.gf_degree == 64 and (self.state_len == 8 or self.state_len == 12))
            or (self.gf_degree == 128 and (self.state_len == 4 or self.state_len == 6))
        )

        GF = self.galois_field()

        x = GF.primitive_element
        ones = GF.Ones((self.state_len, self.state_len)) - GF.Identity(self.state_len)

        if self.gf_degree == 32 and self.state_len == 16:
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
        elif self.gf_degree == 32 and self.state_len == 24:
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
        elif self.gf_degree == 64 and self.state_len == 8:
            diagonal = GF(
                np.diag([x**7 + GF(1), x, x**9, x**7, x**13, x**12, x**14, x**6])
            )
        elif self.gf_degree == 64 and self.state_len == 12:
            diagonal = GF(
                np.diag(
                    [
                        x + GF(1),
                        x**3,
                        x**7,
                        x**13,
                        x**15,
                        GF(1),
                        x**15 + GF(1),
                        x**11,
                        x,
                        x**10 + GF(1),
                        x**12,
                        x**10,
                    ]
                )
            )
        elif self.gf_degree == 128 and self.state_len == 4:
            diagonal = GF(np.diag([x**5, x**13, x**9, x**11]))
        else:
            diagonal = GF(np.diag([x**8, x**10, x**3, x**2, x**11, x**14]))

        return ones + diagonal

    def generate_full_round_matrix(self) -> gf.FieldArray:
        GF = self.galois_field()

        x = GF.primitive_element
        mat4x4 = GF(
            [
                [
                    x**2 + GF(1),
                    x**2 + x + GF(1),
                    1,
                    x + GF(1),
                ],
                [x**2, x**2 + x, 1, 1],
                [
                    1,
                    x + GF(1),
                    x**2 + GF(1),
                    x**2 + x + GF(1),
                ],
                [1, 1, x**2, x**2 + x],
            ]
        )

        if self.state_len == 4:
            return mat4x4
        elif self.state_len == 6:
            return GF(circulant([x**9, 1, x**11, x, x, 1]))
        else:
            tby4 = self.state_len // 4
            blocks = [
                [x * mat4x4 if i == j else mat4x4 for j in range(tby4)]
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

        GF = self.galois_field()

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


Poseidon2b_n32t16 = Poseidon2bParameters(32, 16, 8, 15, 7)
Poseidon2b_n32t24 = Poseidon2bParameters(32, 24, 8, 15, 7)
Poseidon2b_n64t8 = Poseidon2bParameters(64, 8, 8, 29, 7)
Poseidon2b_n64t12 = Poseidon2bParameters(64, 12, 8, 29, 7)
Poseidon2b_n128t4 = Poseidon2bParameters(128, 4, 8, 58, 7)
Poseidon2b_n128t6 = Poseidon2bParameters(128, 6, 8, 58, 7)

if __name__ == "__main__":
    print("This is not an executable module.")
    exit(1)
