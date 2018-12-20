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
from intergalactic.types import MessageType


class HealthcheckView(HTTPMethodView):
    """Healthcheck view class."""

    async def get(self, request):
        return json({"status": "ok"})


class MineBlockView(HTTPMethodView):
    """Mine block view class."""

    async def post(self, request):
        from intergalactic.peer.publisher import broadcast

        # Mine a new block
        block = blockchain.mine_block()
        block_dict = block.to_dict()

        # Add the new block to the blockchain
        blockchain.add_block(block)

        # Broadcast new block to the network
        await broadcast({
            "type": MessageType.NOTIFY_NEW_BLOCKS.value,
            "data": [block_dict]
        })

        return json({"block": block_dict})
