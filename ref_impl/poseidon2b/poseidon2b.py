from .params import Poseidon2bParameters
import galois as gf
import numpy as np


class Poseidon2b:
    """
    Arithmetization friendly Poseidon2b permutation, over binary extension field GF(2^n).
    """

    def __init__(self, params: Poseidon2bParameters) -> None:
        """
        Given a valid Poseidon2b instance, defined in `.params` module, this init function will compute round constants, full round matrix and partial round matrix. Post init, one can invoke the permute function to permute input state.
        """
        self._ROUND_CONSTANTS = params.generate_round_constants()
        self._FULL_ROUND_MATRIX = params.generate_full_round_matrix()
        self._PARTIAL_ROUND_MATRIX = params.generate_partial_round_matrix()

        self._GF = params.galois_field()
        self._params = params

    def _AddRoundCons(self, state: gf.FieldArray, ridx: int) -> gf.FieldArray:
        """
        Addition of round constants into all/ some branches of the state. Collects inspiration from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.sage#L263-L272.
        Note, when applying full round, all branches are added with round constants. While during a partial round, only the first branch is added with corresponding round constant. But to abstract it away, we choose to zeroize
        all partial round's non-first branch round constants.
        """
        return state + self._ROUND_CONSTANTS[ridx]

    def _SubWordsRF(self, state: gf.FieldArray) -> gf.FieldArray:
        """
        Applies power map exponent on all branches, during a full round. Collects inspiration from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.sage#L274-L283.
        """
        return self._GF(list(map(lambda x: x**self._params.alpha, state)))

    def _SubWordsRP(self, state: gf.FieldArray) -> gf.FieldArray:
        """
        Applies power map exponent only on the first branch, during a partial round. Collects inspiration from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.sage#L285-L295.
        """
        state[0] = state[0] ** self._params.alpha
        return state

    def _RoundFull(self, state: gf.FieldArray, ridx: int) -> gf.FieldArray:
        """
        Applies a full round on the permutation state, returning updated state. Collects inspiration from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.sage#L297-L314.
        """
        state = self._AddRoundCons(state, ridx)
        state = self._SubWordsRF(state)
        state = np.matmul(self._FULL_ROUND_MATRIX, state)

        return state

    def _RoundPartial(self, state: gf.FieldArray, ridx: int) -> gf.FieldArray:
        """
        Applies a partial round of the permutation, returning updated state. Collects inspiration from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.sage#L316-L333.
        """
        state = self._AddRoundCons(state, ridx)
        state = self._SubWordsRP(state)
        state = np.matmul(self._PARTIAL_ROUND_MATRIX, state)

        return state

    def permute(self, state: gf.FieldArray) -> gf.FieldArray:
        """
        Applies Poseidon2b permutation on input state, returning updated state. Collects inspiration from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.sage#L335-L388.
        """
        assert self._params.state_len == len(state)
        state = np.matmul(self._FULL_ROUND_MATRIX, state)

        for ridx in range(self._params.num_total_rounds()):
            if self._params.is_full_round(ridx):
                state = self._RoundFull(state, ridx)
            else:
                state = self._RoundPartial(state, ridx)

        return state


if __name__ == "__main__":
    print("This is not an executable module.")
    exit(1)
