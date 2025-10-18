#!/usr/bin/python

from poseidon2b import (
    Poseidon2b_n32t16,
    Poseidon2b_n32t24,
    Poseidon2b_n64t8,
    Poseidon2b_n64t12,
    Poseidon2b_n128t6,
    Poseidon2b_n128t4,
    Poseidon2bParameters,
)


def print_matrix(np_mat):
    for row in map(lambda row: list(map(lambda lane: int(lane), row)), np_mat):
        print(row)


def print_params(pos2b: Poseidon2bParameters):
    print(f"Poseidon2b_n{pos2b.gf_degree}t{pos2b.state_len}:\n")
    print(
        f"n = {pos2b.gf_degree}\nt = {pos2b.state_len}\nrF = {pos2b.num_full_rounds}\nrP = {pos2b.num_partial_rounds}\nr = {pos2b.num_total_rounds()}\nalpha = {pos2b.alpha}\n"
    )

    print("Binary extension field properties:")
    print(pos2b.galois_field().properties)
    print()

    full_round_matrix = pos2b.generate_full_round_matrix()
    print(f"Full Round Matrix ({full_round_matrix.shape}):")
    print_matrix(full_round_matrix)
    print()

    partial_round_matrix = pos2b.generate_partial_round_matrix()
    print(f"Partial Round Matrix ({partial_round_matrix.shape}):")
    print_matrix(partial_round_matrix)
    print()

    round_constants = pos2b.generate_round_constants()
    print(f"Round Constants Matrix ({round_constants.shape}):")
    print_matrix(round_constants)
    print()


def main():
    print_params(Poseidon2b_n32t16)
    print("------------------------------------------------------------------------------------------------------------\n")
    print_params(Poseidon2b_n32t24)
    print("------------------------------------------------------------------------------------------------------------\n")
    print_params(Poseidon2b_n64t8)
    print("------------------------------------------------------------------------------------------------------------\n")
    print_params(Poseidon2b_n64t12)
    print("------------------------------------------------------------------------------------------------------------\n")
    print_params(Poseidon2b_n128t4)
    print("------------------------------------------------------------------------------------------------------------\n")
    print_params(Poseidon2b_n128t6)


if __name__ == "__main__":
    main()
