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


def create_hash(index, previous_hash, timestamp, transactions):
    return hashlib.sha256(json.dumps({
        "index": int(index),
        "previous_hash": str(previous_hash),
        "timestamp": str(timestamp),
        "transactions": [{
            "sender": str(transaction.sender),
            "recipient": str(transaction.recipient),
            "amount": float(transaction.amount),
        } for transaction in transactions]
    }).encode('utf-8')).hexdigest()
