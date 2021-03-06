#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2014-2016, German Aerospace Center (DLR)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Authors:
# - 2014-2016, Fabian Greif (DLR RY-AVS)

import re
import commands


def detect_gcc_version(env, gcc=None):
    """"Detect the version of the used GCC.

    Used env['CXX'] as reference. A version string such as 4.4.3 is
    transformed into an integer with two characters per level, here: 40403.

    Examples:
      4.9.2         -> 40902
      4.7           -> 40700
      4.6.5         -> 40605
      4.5.3-or32-1  -> 40503
      4.3.10        -> 40310
    """""
    if gcc is None:
        gcc = env['CXX']

    v = commands.getoutput(gcc + ' -dumpversion')  # v = 4.5.3-or32-1
    version = re.match("^(\d)\.(\d)\.(\d)(-(.*))$", v)
    if version:
        compiler_version = int(version.group(1)) * 10000 + \
                           int(version.group(2)) * 100 + \
                           int(version.group(3))
    else:
        # Compiler version could not be detected
        compiler_version = 0

    return compiler_version


def generate(env, **kw):
    env.AddMethod(detect_gcc_version, 'DetectGccVersion')


def exists(env):
    return True
