# How to use Poseidon2b Python module?

- Setup Python virtual environment and fetch all dependencies by running following command from root of this repository.

```bash
make setup
```

- Enable Python virtual environment.

```bash
source .venv/bin/activate
pushd ref_impl
```

- Open Python REPL console to import Poseidon2b module and use it for permuting inputs.

```python
>>> import poseidon2b
>>> params = poseidon2b.Poseidon2b_n32t16
>>> gf = params.galois_field()
>>> in_state = gf(list(range(params.state_len)))
>>> in_state
GF([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15],
   order=2^32)
>>> instance = poseidon2b.Poseidon2b(params)
>>> instance.permute(in_state)
GF([3263689815, 3510016260,  531948390,  201633991, 2369968409,
    2911726907, 3767115820, 1283168574, 3383130628,  115255156,
    1084253133,  337390485, 2474582269, 1077148670, 1561443687,
    3531824307], order=2^32)
>>>
```

- When done, leave reference implementation directory and deactivate Python virtual environment.

```bash
popd
deactivate
```
