# Copyright 2018 Rob Moorman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import binascii
import hashlib
import json

from Crypto import Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from datetime import timezone, datetime

from intergalactic.blockchain.block import Block
from intergalactic.blockchain.hasher import BlockHasher, TransactionHasher
from intergalactic.blockchain.pow import ProofOfWork
from intergalactic.blockchain.validator import BlockchainValidator
from intergalactic.blockchain.transaction import Transaction


class Blockchain:
    def __init__(self):
        self.blocks = []
        self.blocks.append(self.create_genesis_block())
        self.transactions = []

    def create_genesis_block(self) -> Block:
        index = 0
        previous_hash = "0"
        timestamp = 1545317034183
        merkle_root = BlockHasher().create_merkle_root([])
        proof = 0
        hash = BlockHasher().create_hash(
            index, previous_hash, timestamp, merkle_root, proof)
        block = Block(
            index, previous_hash, timestamp, hash, merkle_root, 0, [])
        return block

    def mine_block(self):
        latest_block = self.get_latest_block()
        index = latest_block.index + 1
        previous_hash = latest_block.hash
        timestamp = self.get_timestamp()
        merkle_root = BlockHasher().create_merkle_root(self.transactions)
        proof = ProofOfWork().get_proof(previous_hash, merkle_root)
        hash = BlockHasher().create_hash(
            index, previous_hash, timestamp, merkle_root, proof)
        block = Block(
            index, previous_hash, timestamp, hash, merkle_root, proof,
            self.transactions)

        self.add_block(block)
        self.reset_transactions()

        return block

    def create_transaction(self, sender: str, recipient: str, amount: float, timestamp: int, signature: str):
        hash = TransactionHasher().create_hash(
            sender, recipient, amount, timestamp)
        transaction = Transaction(hash, sender, recipient, amount, timestamp, signature)
        verified = self.verify_transaction_signature(sender, transaction, signature)

        if verified:
            self.add_transaction(transaction)
            return transaction

        return None

    def get_blocks(self):
        return self.blocks

    def get_latest_block(self) -> Block:
        return self.blocks[-1]

    def get_block_height(self) -> int:
        return len(self.blocks)

    def get_transactions(self):
        return self.transactions

    def get_timestamp(self) -> int:
        return int(datetime.now(tz=timezone.utc).timestamp() * 1000)

    def add_block(self, block: Block):
        self.blocks.append(block)

    def replace_blocks(self, blocks):
        self.blocks = blocks

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def reset_transactions(self):
        self.transactions = []

    def verify_transaction_signature(self, sender: str, transaction: Transaction, signature: str) -> bool:
        try:
            pk = RSA.importKey(binascii.unhexlify(sender))
            signer = PKCS1_v1_5.new(pk)
            hash = SHA.new(str({
                "sender": transaction.sender,
                "recipient": transaction.recipient,
                "amount": transaction.amount,
                "timestamp": transaction.timestamp
            }).encode('utf-8'))
            verified = signer.verify(hash, binascii.unhexlify(signature))
            return verified
        except:
            pass
        return False

    def validate_chain(self, chain):
        return BlockchainValidator().validate(chain)


blockchain = Blockchain()
