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
from datetime import timezone, datetime

from intergalactic.blockchain import hasher
from intergalactic.blockchain.block import Block


class Blockchain:
    def __init__(self):
        self.blocks = []
        self.blocks.append(self.create_genesis_block())

    def create_genesis_block(self):
        index = 0
        previous_hash = "0"
        timestamp = 1545317034183
        hash = hasher.create_hash(index, previous_hash, timestamp)
        block = Block(index, previous_hash, timestamp, hash)
        return block

    def mine_block(self):
        latest_block = self.get_latest_block()
        index = latest_block.index + 1
        previous_hash = latest_block.hash
        timestamp = self.get_timestamp()
        hash = hasher.create_hash(index, previous_hash, timestamp)
        block = Block(index, previous_hash, timestamp, hash)
        return block

    def get_blocks(self):
        return self.blocks

    def get_latest_block(self):
        return self.blocks[-1]

    def get_block_height(self):
        return len(self.blocks)

    def get_timestamp(self):
        return int(datetime.now(tz=timezone.utc).timestamp() * 1000)

    def add_block(self, block):
        self.blocks.append(block)

    def replace_blocks(self, blocks):
        self.blocks = blocks


blockchain = Blockchain()
