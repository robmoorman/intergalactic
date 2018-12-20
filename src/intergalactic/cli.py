#!/usr/bin/env python
#
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

import os
import sys
import argparse

from intergalactic import bootstrapper
from intergalactic.utils import logging

BANNER = """
.___        __                            .__                 __  .__
|   | _____/  |_  ___________  _________  |  | _____    _____/  |_|__| ____
|   |/    \   __\/ __ \_  __ \/ ___\__  \ |  | \__  \ _/ ___\   __\  |/ ___\
|   |   |  \  | \  ___/|  | \/ /_/  > __ \|  |__/ __ \\  \___|  | |  \  \___
|___|___|  /__|  \___  >__|  \___  (____  /____(____  /\___  >__| |__|\___  >
         \/          \/     /_____/     \/          \/     \/             \/
"""
COMMANDS = ["run", "reset_db"]


def execute():
    parser = argparse.ArgumentParser(
        description="Intergalactic Command-line interface.")
    parser.add_argument(
        "command", type=str, choices=COMMANDS, help="Command to execute")
    args = parser.parse_args()
    {
        "run": bootstrapper.run,
        "reset_db": lambda: sys.exit(0)
    }[args.command]()


if __name__ == "__main__":
    execute()
