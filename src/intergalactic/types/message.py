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

from enum import IntEnum


class MessageType(IntEnum):
    PING = 0
    PONG = 1

    NOTIFY_NEW_BLOCKS = 100
    NOTIFY_NEW_PEERS = 200

    QUERY_CONNECTED_PEERS = 300
    QUERY_LATEST_BLOCK = 400
    QUERY_ALL_BLOCKS = 500
