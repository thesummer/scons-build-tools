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
# - 2017, Jan Sommer (DLR SC-SRV)

from SCons.Script import *


def generate(env, **kw):
    env['PROGSUFFIX'] = ''
    env['ARCHITECTURE'] = 'xtensa'
    env.SetDefault(OS = 'none')
    
    env.SetDefault(COMPILERPREFIX='xtensa-lx106-elf-')

    env.SetDefault(CCFLAGS_target=['-mlongcalls', '-mtext-section-literals', ])
    env.SetDefault(CCFLAGS_optimize=['-O2', 
                                     '-ffunction-sections', 
                                     '-fdata-sections',
                                     '-fno-inline-functions',
                                     '-nostdlib',
                                     '-fno-builtin-printf',
                                     '-fno-jump-tables'])

    env.SetDefault(CXXFLAGS_dialect=['-fno-rtti', '-fno-exceptions', ])

    env.SetDefault(LINKFLAGS_target=['-Wl,-EL',
                                      "-Os",
                                      "-nostdlib",
                                      "-Wl,--no-check-sections",
                                      "-u", "call_user_start",
                                      "-Wl,-static",
                                      "-Wl,--gc-sections"])

    env.SetDefault(CPPDEFINES='ICACHE_FLASH')

    env.Tool('settings_gcc_default_internal')
    
def exists(env):
    return env.Detect('gcc')
