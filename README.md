# poseidon2b

Arithmetization Friendly Hash Function Poseidon over Binary Extension Field

## Introduction

Poseidon2b[^3] is an arithmetization friendly hash function, defined over binary extension field i.e. $GF(2^n)$. It extends well known Poseidon[^1] hash function to binary fields. Poseidon was originally defined over relatively large prime fields, generally those which are used in pairing-friendly elliptic curves. It has been a popular choice in developing zkSNARKs and zkSTARKs. Recently an optimization over Poseidon, Posiedon2[^2] was proposed, targeted towards smaller prime fields. As they are a popular choice in designing modern SNARKS.

Poseidon2b has following two goals.

- Being as fast as possible on a commodity CPU by using sparse constants and low-degree power maps.
- Being fast in a proof system by minimizing the number of algebraic constraints.

In this repository, we are maintaining a Python reference implementation of $Poseidon2b^\pi$ permutation. The Poseidon2b paper already comes with a sage reference implementation[^4]. The goal of this Python implementation is to provide the community with another implementation in different language as reference. We use this implementation to generate parameters such partial/ full round matrices and round constants for all proposed Poseidon2b instances in table 1 of Poseidon2b[^3]. This is to help future implementations with Poseidon2b parameters. Poseidon2b reference implementation comes with a Jupyter notebook[^5], which lists one test vector for each proposed parameter set. We generate 100 test vectors for each parameter set, hoping it will help future Poseidon2b implementations.

We plan to also develop an optimized Rust implementation of Poseidon2b, using carry-less multiplication intrinsics.

[^1]: Lorenzo Grassi, Dmitry Khovratovich, Christian Rechberger, Arnab Roy, and
Markus Schofnegger. “Poseidon: A New Hash Function for Zero-Knowledge
Proof Systems”. In: USENIX Security Symposium. USENIX Association, 2021,
pp. 519–535. url: <https://www.usenix.org/conference/usenixsecurity21/presentation/grassi>

[^2]: Lorenzo Grassi, Dmitry Khovratovich, and Markus Schofnegger. Poseidon2:
A Faster Version of the Poseidon Hash Function. IACR Cryptology ePrint
Archive, Paper 2023/323. 2023. url: <https://eprint.iacr.org/2023/323>

[^3]: Lorenzo Grassi and Dmitry Khovratovich and Katharina Koschatko and Christian Rechberger and Markus Schofnegger and Verena Schroppel Poseidon2b: A Binary Field Version of Poseidon2. IACR Cryptology ePrint Archive, Paper 2025/058. 2025. url: <https://eprint.iacr.org/2025/058>

[^4]: Poseidon2b: A Binary Field Version of Poseidon2. url: <https://github.com/Poseidon-Hash/Poseidon2b/tree/aee285ce5f672bb70a4b25fa6d55d5706f755b76>

[^5]: Poseidon2b: A Binary Field Version of Poseidon2. url: <https://github.com/Poseidon-Hash/Poseidon2b/blob/aee285ce5f672bb70a4b25fa6d55d5706f755b76/sage-ref/Poseidon2b.ipynb>

## Testing

For ensuring compatibility of this Poseidon2b Python implementation with sage implementation[^4], coming from the submission team, run following command from the root of this repository.

```bash
make setup # Sets up Python virtual environment and fetches all dependencies
make test  # Runs known answer tests to self-check
```

## Scripts

### Poseidon2b Parameters

You can use this Poseidon2b Python implementation for generating detailed parameters for all proposed parameter sets. Run the following command to generate it yourself. Or you can just use the generated file [./ref_impl/poseidon2b_parameters.txt](./ref_impl/poseidon2b_parameters.txt).

```bash
make setup      # If you haven't done it yet
make gen_params # Generates all parameter sets, writing to a text file
```

```bash
$ sha256sum ref_impl/poseidon2b_parameters.txt
8c5bac858425837f94c1bb81808d72409fcf9b52952235a64ed559ab6d2cd4b7  ref_impl/poseidon2b_parameters.txt
```

<details>

<summary>Click to expand generated parameters (partial) file.</summary>

```bash
Poseidon2b_n32t16:

n = 32
t = 16
rF = 8
rP = 15
r = 23
alpha = 7

Binary extension field properties:
Galois Field:
  name: GF(2^32)
  characteristic: 2
  degree: 32
  order: 4294967296
  irreducible_poly: x^32 + x^15 + x^9 + x^7 + x^4 + x^3 + 1
  is_primitive_poly: True
  primitive_element: x

Full Round Matrix ((16, 16)):
[10, 14, 2, 6, 5, 7, 1, 3, 5, 7, 1, 3, 5, 7, 1, 3]
[8, 12, 2, 2, 4, 6, 1, 1, 4, 6, 1, 1, 4, 6, 1, 1]
[2, 6, 10, 14, 1, 3, 5, 7, 1, 3, 5, 7, 1, 3, 5, 7]
[2, 2, 8, 12, 1, 1, 4, 6, 1, 1, 4, 6, 1, 1, 4, 6]
[5, 7, 1, 3, 10, 14, 2, 6, 5, 7, 1, 3, 5, 7, 1, 3]
[4, 6, 1, 1, 8, 12, 2, 2, 4, 6, 1, 1, 4, 6, 1, 1]
[1, 3, 5, 7, 2, 6, 10, 14, 1, 3, 5, 7, 1, 3, 5, 7]
[1, 1, 4, 6, 2, 2, 8, 12, 1, 1, 4, 6, 1, 1, 4, 6]
[5, 7, 1, 3, 5, 7, 1, 3, 10, 14, 2, 6, 5, 7, 1, 3]
[4, 6, 1, 1, 4, 6, 1, 1, 8, 12, 2, 2, 4, 6, 1, 1]
[1, 3, 5, 7, 1, 3, 5, 7, 2, 6, 10, 14, 1, 3, 5, 7]
[1, 1, 4, 6, 1, 1, 4, 6, 2, 2, 8, 12, 1, 1, 4, 6]
[5, 7, 1, 3, 5, 7, 1, 3, 5, 7, 1, 3, 10, 14, 2, 6]
[4, 6, 1, 1, 4, 6, 1, 1, 4, 6, 1, 1, 8, 12, 2, 2]
[1, 3, 5, 7, 1, 3, 5, 7, 1, 3, 5, 7, 2, 6, 10, 14]
[1, 1, 4, 6, 1, 1, 4, 6, 1, 1, 4, 6, 2, 2, 8, 12]

...
```

</details>

### Poseidon2b Known Answer Tests

Generate test vectors for all proposed Poseidon2b parameters by running following command. Or you can just use pre-computed KATs from [./kats](./kats) directory.

```bash
make setup    # If you haven't done it yet
make gen_kats # Generated KATs are placed inside ./kats directory
```

```bash
$ sha256sum kats/*
75e4fb9aa4d9bfb5e6e7a6ff4b80696f861bf01938d731b159e07f33d0af9a09  kats/poseidon2b_n128t4.kat
1152464b1cdbecd86b8435ba26aa23f1278f2a159db9b8a5ba98b8b77b223e99  kats/poseidon2b_n128t6.kat
c968b1365add89bf3d788e005a348a1524680f1e25c13cb5217e6d0e2802eef6  kats/poseidon2b_n32t16.kat
7fcc833471c90fa7aadd58300390b7dec89159310f0e357ad14012db9ed62d1e  kats/poseidon2b_n32t24.kat
355aa8fd414696dea477c06fa2236f552c7feedc31688b7bfcc23c3b2f8e7653  kats/poseidon2b_n64t12.kat
ba4724c8c11cffc35883e53da40c5390447f3c5667e07a085d9ea61008c372ff  kats/poseidon2b_n64t8.kat
```
