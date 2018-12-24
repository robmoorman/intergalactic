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

import hashlib
import json


class BlockHasher:
    def __init__(self):
        pass

    def create_hash(self, index: int, previous_hash: str, timestamp: int, merkle_root: str, proof: int) -> str:
        return hashlib.sha256(json.dumps({
            "index": index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "proof": proof,
            "merkle_root": merkle_root
        }).encode('utf-8')).hexdigest()

    def create_merkle_root(self, transactions) -> str:
        hashes = [x.hash for x in transactions]
        return hashlib.sha256(json.dumps(hashes).encode('utf-8')).hexdigest()


class TransactionHasher:
    def __init__(self):
        pass

    def create_hash(self, sender: str, recipient: str, amount: float, timestamp: int) -> str:
        return hashlib.sha256(json.dumps({
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "timestamp": timestamp
        }).encode('utf-8')).hexdigest()
