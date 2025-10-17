from Crypto.Hash import TurboSHAKE256
import math

SHAKE_INIT = "Poseidon2b"


class SHAKEUtils:
    def __init__(self, gf_degree):
        self.init_shake = SHAKE_INIT
        self.field_size = 2**gf_degree
        self.num_bytes = math.ceil(self.field_size.bit_length() / 8)

    def init_shake_reader(self):
        shake = TurboSHAKE256.new(domain=0x1F)
        shake.update(self.init_shake.encode("utf-8"))
        for value in self.get_field_size_in_chunks():
            shake.update(int(value).to_bytes(length=8, byteorder="little"))
        return shake

    def get_field_size_in_chunks(self):
        o = self.field_size
        order = []
        while o != 0:
            o_ = o & (2**64 - 1)
            order.append(o_)
            o >>= 64
        return order

    def get_field_element_from_shake(self, reader):
        while True:
            buf = bytearray(reader.read(self.num_bytes))
            value = int.from_bytes(buf, "little")  # Convert bytes to integer
            if value < self.field_size:  # Ensure the value is within the field
                return value

    def get_random_elements(self, num_values, shake):
        return [self.get_field_element_from_shake(shake) for _ in range(num_values)]


if __name__ == "__main__":
    print("This is not an executable module.")
    exit(1)
