import pytest


def test_genesis_block(blockchain):
    block = blockchain.get_latest_block()
    assert len(block.transactions) == 0
