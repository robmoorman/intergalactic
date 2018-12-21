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

from intergalactic import settings
from intergalactic.api import views
from intergalactic.peer import handlers, subscriber


class Server:
    """Server."""

    def __init__(self):
        self.app = Sanic()

        self.init_peer_subscribers(settings.BOOTSTRAP_PEERS.split(","))

        self.app.add_route(views.HealthcheckView.as_view(), '/healthcheck/')
        self.app.add_route(views.MineBlockView.as_view(), '/mine_block/')
        self.app.add_route(views.AddTransactionView.as_view(), '/add_transaction/')
        self.app.add_websocket_route(handlers.peer_to_peer_handler, '/')

    def init_peer_subscribers(self, peers):
        for peer in peers:
            if peer != "":
                self.app.add_task(subscriber.subscribe_to_peer(peer))

    def serve(self, debug=False):
        self.app.run(
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            debug=debug
        )
