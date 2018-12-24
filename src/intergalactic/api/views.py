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

from sanic import Sanic
from sanic.response import json
from sanic.views import HTTPMethodView

from intergalactic import settings
from intergalactic.blockchain.blockchain import blockchain
from intergalactic.peer.publisher import broadcast
from intergalactic.types import MessageType


class HealthcheckView(HTTPMethodView):
    """Healthcheck view class."""

    async def get(self, request):
        return json({"status": "ok"})


class MineBlockView(HTTPMethodView):
    """Mine block view class."""

    async def post(self, request):
        # Mine a new block
        block = blockchain.mine_block()
        block_dict = block.to_dict()

        # Broadcast new block to the network
        await broadcast({
            "type": MessageType.NOTIFY_NEW_BLOCKS.value,
            "data": [block_dict]
        })

        return json({"block": block_dict})


class AddTransactionView(HTTPMethodView):
    """Add transation view class."""

    async def post(self, request):
        data = request.json
        transaction = None

        if data is not None:
            sender = data["sender"]
            recipient = data["recipient"]
            amount = data["amount"]
            timestamp = data["timestamp"]
            signature = data["signature"]

            # Create a new transaction
            transaction = blockchain.create_transaction(
                sender, recipient, amount, timestamp, signature)

        if not transaction:
            return json({
                "error": "Invalid transaction"
            }, status=400)

        transaction_dict = transaction.to_dict()

        # Broadcast new transaction to the network
        await broadcast({
            "type": MessageType.NOTIFY_NEW_TRANSACTION.value,
            "data": transaction_dict
        })

        return json({"transaction": transaction_dict})
