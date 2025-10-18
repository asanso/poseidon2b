#!/usr/bin/python

from poseidon2b import (
    Poseidon2b_n32t16,
    Poseidon2b_n32t24,
    Poseidon2b_n64t8,
    Poseidon2b_n64t12,
    Poseidon2b_n128t6,
    Poseidon2b_n128t4,
    Poseidon2bParameters,
    Poseidon2b,
)
import random
from Crypto.Hash import SHA3_256

# Fix seed for reproducing the same Known Answer Tests for Poseidon2b
random.seed(7)
NUM_TEST_VECTORS_PER_POSEIDON2B_INSTANCE = 100


def compute_sha3_256_digest_of_file(filename: str) -> str:
    hasher = SHA3_256.new()

    with open(filename, "rb") as fd:
        hasher.update(fd.read())

    return hasher.hexdigest()


def generate_and_write_kats(pos2b_params: Poseidon2bParameters) -> str:
    kat_filename = f"poseidon2b_n{pos2b_params.gf_degree}t{pos2b_params.state_len}.kat"
    pos2b_instance = Poseidon2b(pos2b_params)

    GF = pos2b_params.galois_field()
    GF_MIN_VAL = 0
    GF_MAX_VAL = GF.order - 1

    with open(kat_filename, "wt") as fd:
        for kat_idx in range(NUM_TEST_VECTORS_PER_POSEIDON2B_INSTANCE):
            fd.write(f"Index = {kat_idx}\n")

            in_state = GF(
                list(
                    map(
                        lambda _: random.randint(GF_MIN_VAL, GF_MAX_VAL),
                        range(pos2b_params.state_len),
                    )
                )
            )
            fd.write(f"Input State = {list(map(lambda x: int(x), in_state))}\n")

            out_state = pos2b_instance.permute(in_state)
            fd.write(f"Output State = {list(map(lambda x: int(x), out_state))}\n\n")

    return compute_sha3_256_digest_of_file(kat_filename)


def main():
    print(
        f"✅ Generated KATs for Poseidon2b_n32t16 (SHA3_256 digest: {generate_and_write_kats(Poseidon2b_n32t16)})"
    )
    print(
        f"✅ Generated KATs for Poseidon2b_n32t24 (SHA3_256 digest: {generate_and_write_kats(Poseidon2b_n32t24)})"
    )

    print(
        f"✅ Generated KATs for Poseidon2b_n64t8 (SHA3_256 digest: {generate_and_write_kats(Poseidon2b_n64t8)})"
    )
    print(
        f"✅ Generated KATs for Poseidon2b_n64t12 (SHA3_256 digest: {generate_and_write_kats(Poseidon2b_n64t12)})"
    )

    print(
        f"✅ Generated KATs for Poseidon2b_n128t4 (SHA3_256 digest: {generate_and_write_kats(Poseidon2b_n128t4)})"
    )
    print(
        f"✅ Generated KATs for Poseidon2b_n128t6 (SHA3_256 digest: {generate_and_write_kats(Poseidon2b_n128t6)})"
    )


if __name__ == "__main__":
    main()
