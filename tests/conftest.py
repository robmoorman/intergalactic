import pytest

from intergalactic.blockchain.block import Block
from intergalactic.blockchain.blockchain import Blockchain
from intergalactic.blockchain.transaction import Transaction

merkle_root = "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"


@pytest.fixture
def blockchain():
    return Blockchain()


@pytest.fixture
def valid_chain():
    return [
        Block(0, "", 0, "20f08c546b56ca2a8aaeafd7ed0c99d99dceeeb2aa907b923ccddd087ba23084", merkle_root, 39710, []),
        Block(1, "20f08c546b56ca2a8aaeafd7ed0c99d99dceeeb2aa907b923ccddd087ba23084", 100, "73c5458c31a0f29f99779538b714feace1ddf25db1bc681138d22bae0557f3ca", merkle_root, 64938, []),
        Block(2, "73c5458c31a0f29f99779538b714feace1ddf25db1bc681138d22bae0557f3ca", 200, "529c177087733d4f661fae3487462bf7d7940e5534a3785e6243af74d90bd846", merkle_root, 12659, []),
        Block(3, "529c177087733d4f661fae3487462bf7d7940e5534a3785e6243af74d90bd846", 300, "d74f61a89d6c362c1239eec0f9295d606bf7ff3e30339ac18032a3ff59d1dc10", merkle_root, 46038, []),
    ]


@pytest.fixture
def invalid_chain_order():
    return [
        Block(0, "", 0, "20f08c546b56ca2a8aaeafd7ed0c99d99dceeeb2aa907b923ccddd087ba23084", merkle_root, 39710, []),
        Block(2, "73c5458c31a0f29f99779538b714feace1ddf25db1bc681138d22bae0557f3ca", 200, "529c177087733d4f661fae3487462bf7d7940e5534a3785e6243af74d90bd846", merkle_root, 12659, []),
        Block(1, "20f08c546b56ca2a8aaeafd7ed0c99d99dceeeb2aa907b923ccddd087ba23084", 100, "73c5458c31a0f29f99779538b714feace1ddf25db1bc681138d22bae0557f3ca", merkle_root, 64938, []),
    ]


@pytest.fixture
def invalid_chain_proof_of_work():
    return [
        Block(0, "", 0, "20f08c546b56ca2a8aaeafd7ed0c99d99dceeeb2aa907b923ccddd087ba23084", merkle_root, 39710, []),
        Block(1, "20f08c546b56ca2a8aaeafd7ed0c99d99dceeeb2aa907b923ccddd087ba23084", 100, "73c5458c31a0f29f99779538b714feace1ddf25db1bc681138d22bae0557f3ca", merkle_root, 64938, []),
        Block(2, "73c5458c31a0f29f99779538b714feace1ddf25db1bc681138d22bae0557f3ca", 200, "529c177087733d4f661fae3487462bf7d7940e5534a3785e6243af74d90bd846", merkle_root, 12659, []),
        # Last item proof is invalid (should be 46038)
        Block(3, "529c177087733d4f661fae3487462bf7d7940e5534a3785e6243af74d90bd846", 300, "d74f61a89d6c362c1239eec0f9295d606bf7ff3e30339ac18032a3ff59d1dc10", merkle_root, 1337, []),
    ]
