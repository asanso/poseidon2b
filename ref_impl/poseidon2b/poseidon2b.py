from .params import Poseidon2bParameters
import galois as gf
import numpy as np


class Poseidon2b:
    def __init__(self, params: Poseidon2bParameters) -> None:
        self._ROUND_CONSTANTS = params.generate_round_constants()
        self._FULL_ROUND_MATRIX = params.generate_full_round_matrix()
        self._PARTIAL_ROUND_MATRIX = params.generate_partial_round_matrix()

        self._GF = params.galois_field()
        self._params = params

    def _AddRoundCons(self, state: gf.FieldArray, ridx: int) -> gf.FieldArray:
        return state + self._ROUND_CONSTANTS[ridx]

    def _SubWordsRF(self, state: gf.FieldArray) -> gf.FieldArray:
        return self._GF(list(map(lambda x: x**self._params.alpha, state)))

    def _SubWordsRP(self, state: gf.FieldArray) -> gf.FieldArray:
        state[0] = state[0] ** self._params.alpha
        return state

    def _RoundFull(self, state: gf.FieldArray, ridx: int) -> gf.FieldArray:
        state = self._AddRoundCons(state, ridx)
        state = self._SubWordsRF(state)
        state = np.matmul(self._FULL_ROUND_MATRIX, state)

        return state

    def _RoundPartial(self, state: gf.FieldArray, ridx: int) -> gf.FieldArray:
        state = self._AddRoundCons(state, ridx)
        state = self._SubWordsRP(state)
        state = np.matmul(self._PARTIAL_ROUND_MATRIX, state)

        return state

    def permute(self, state: gf.FieldArray) -> gf.FieldArray:
        state = np.matmul(self._FULL_ROUND_MATRIX, state)

        for ridx in range(self._params.num_total_rounds()):
            if self._params.is_full_round(ridx):  # full rounds
                state = self._RoundFull(state, ridx)
            else:  # partial rounds
                state = self._RoundPartial(state, ridx)

        return state


if __name__ == "__main__":
    print("This is not an executable module.")
    exit(1)
