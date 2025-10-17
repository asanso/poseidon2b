from .params import Poseidon2bPermutationParameters
import galois as gf
import numpy as np


class Poseidon2b:
    def __init__(self, params: Poseidon2bPermutationParameters) -> None:
        self.ROUND_CONSTANTS = params.generate_round_constants()
        self.FULL_ROUND_MATRIX = params.generate_full_round_matrix()
        self.PARTIAL_ROUND_MATRIX = params.generate_partial_round_matrix()

        self.GF = gf.GF(2**params.gf_degree)
        self.params = params

    def AddRoundCons(self, state: gf.FieldArray, ridx: int) -> gf.FieldArray:
        return state + self.ROUND_CONSTANTS[ridx]

    def SubWordsRF(self, state: gf.FieldArray) -> gf.FieldArray:
        return self.GF(list(map(lambda x: x**self.params.alpha, state)))

    def SubWordsRP(self, state: gf.FieldArray) -> gf.FieldArray:
        state[0] = state[0] ** self.params.alpha
        return state

    def RoundFull(self, state: gf.FieldArray, ridx: int) -> gf.FieldArray:
        state = self.AddRoundCons(state, ridx)
        state = self.SubWordsRF(state)
        state = np.matmul(self.FULL_ROUND_MATRIX, state)

        return state

    def RoundPartial(self, state: gf.FieldArray, ridx: int) -> gf.FieldArray:
        state = self.AddRoundCons(state, ridx)
        state = self.SubWordsRP(state)
        state = np.matmul(self.PARTIAL_ROUND_MATRIX, state)

        return state

    def permute(self, state: gf.FieldArray) -> gf.FieldArray:
        state = np.matmul(self.FULL_ROUND_MATRIX, state)

        for ridx in range(self.params.num_total_rounds()):
            if self.params.is_full_round(ridx):  # full rounds
                state = self.RoundFull(state, ridx)
            else:  # partial rounds
                state = self.RoundPartial(state, ridx)

        return state


if __name__ == "__main__":
    print("This is not an executable module.")
    exit(1)
