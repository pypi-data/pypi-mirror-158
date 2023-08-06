# -*- coding: utf-8 -*-
# Copyright 2021-2022, Hojin Koh
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
from contextlib import contextmanager
from pathlib import Path
from plumbum import FG, local

from .logging import logger

class MixinCmdUtilities(object):

    # Execute to get a plumbum object
    def ex(self, chain):
        logger.info("EX: {}".format(chain))
        chain & FG

    # Just change dir
    def cd(self, path):
        os.chdir(path)

    # Change directory within a context
    @contextmanager
    def chdir(self, path):
        dirCurrent = Path.cwd()
        os.chdir(path)
        yield path
        os.chdir(dirCurrent)

    # Change environment within a context
    @contextmanager
    def env(self, *args, **kwargs):
        with self.local.env(*args, **kwargs):
            yield

    # Produce plumbum objects
    @property
    def cmd(self):
        return local.cmd

    @property
    def local(self):
        return local
