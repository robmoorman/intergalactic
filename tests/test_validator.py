import pytest

from intergalactic.blockchain import validator


def test_validate_chain(valid_chain, invalid_chain_order, invalid_chain_proof_of_work):
    assert validator.BlockchainValidator().validate(valid_chain)
    assert not validator.BlockchainValidator().validate(invalid_chain_order)
    assert not validator.BlockchainValidator().validate(
        invalid_chain_proof_of_work)
