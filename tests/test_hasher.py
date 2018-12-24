import pytest

from intergalactic.blockchain.hasher import BlockHasher

EMPTY_MERKLE_ROOT = "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"


def test_create_hash():
    assert BlockHasher().create_hash(0, "", 0, EMPTY_MERKLE_ROOT, 13782) == "b5787dd90acc175cf53c8bdce5fb6090eb61303f227c41d2deaa33a75d662f6f"
    assert BlockHasher().create_hash(1, "b5787dd90acc175cf53c8bdce5fb6090eb61303f227c41d2deaa33a75d662f6f", 100, EMPTY_MERKLE_ROOT, 13782) == "006c98d5eb2506146a3e59d07da93f2c0958153d4ea644a9114e61c514d713cd"


def test_create_merkle_root():
    assert BlockHasher().create_merkle_root([]) == EMPTY_MERKLE_ROOT
