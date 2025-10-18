from Crypto.Hash import TurboSHAKE256
import math

# Fixed string for initializing TurboSHAKE256 instance, producing Poseidon2b round constants.
# As defined in https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.sage#L446.
SHAKE_INIT = "Poseidon2b"

# This is also the default domain separator value in pycryptodome's TurboSHAKE256 implementation.
# Sometimes it's better to be explicit.
TurboSHAKE256_DOMAIN_SEPARATOR = 0x1F


class SHAKEUtils:
    """
    Utility class for generating Poseidon2b round constants, based on parameter `n`.
    Collects inspiration from https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.sage#L8-L55.
    """

    def __init__(self, gf_degree: int):
        self.gf_order = 2**gf_degree
        self.num_bytes = math.ceil(self.gf_order.bit_length() / 8)

    def init_shake_reader(self):
        shake = TurboSHAKE256.new(domain=TurboSHAKE256_DOMAIN_SEPARATOR)
        shake.update(SHAKE_INIT.encode("utf-8"))

        for chunk in self.get_field_size_in_chunks():
            shake.update(chunk.to_bytes(length=8, byteorder="little"))

        return shake

    def get_field_size_in_chunks(self) -> list[int]:
        CHUNK_SIZE = 64
        MASK = 2**CHUNK_SIZE - 1

        order = self.gf_order
        order_as_chunks = []

        while order != 0:
            order_as_chunks.append(order & MASK)
            order >>= CHUNK_SIZE

        return order_as_chunks

    def get_field_element_from_shake(self, reader) -> int:
        while True:
            buf = bytearray(reader.read(self.num_bytes))
            value = int.from_bytes(buf, "little")
            if (
                value < self.gf_order
            ):  # Rejection sampling. If sampled value doesn't ∈ GF(2^n), it gets discarded.
                return value

    def get_random_elements(self, num_values: int, shake) -> list[int]:
        return list(
            map(lambda _: self.get_field_element_from_shake(shake), range(num_values))
        )


if __name__ == "__main__":
    print("This is not an executable module.")
    exit(1)
