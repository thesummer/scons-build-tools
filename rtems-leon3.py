#!/usr/bin/env python
#
# Copyright (c) 2013, German Aerospace Center (DLR)
# All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the German Aerospace Center (DLR) nor the
#   names of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import commands

from SCons.Script import *

# -----------------------------------------------------------------------------
def generate(env, **kw):
	env.Append(ENV = {'PATH' : os.environ['PATH']})
	env.Tool('gcc')
	env.Tool('g++')
	env.Tool('gnulink')
	env.Tool('ar')
	env.Tool('as')

	env['PROGSUFFIX'] = ''
	
	env['ARCHITECTURE'] = 'leon3'
	env['OS'] = 'rtems'
	
	# used programs
	#env['COMPILERPATH'] = '/opt/rtems-4.10/bin/sparc-rtems-'
	prefix = env.get('COMPILERPATH', 'sparc-rtems-')
	env['CC'] =      prefix + 'gcc'
	env['CXX'] =     prefix + 'g++'
	env['AS'] =      prefix + 'as'
	env['OBJCOPY'] = prefix + 'objcopy'
	env['OBJDUMP'] = prefix + 'objdump'
	env['AR'] =      prefix + 'ar'
	env['NM'] =      prefix + 'nm'
	env['RANLIB'] =  prefix + 'ranlib'
	env['SIZE'] =    prefix + 'size'
	
	v = commands.getoutput(env['CXX'] + ' -dumpversion')	# v = 4.6.1
	v = [int(x) for x in v.split('.')]						# v = [4, 6, 1]
	compiler_version = v[0] * 10000 + v[1] * 100 + v[2]		# v = 40601
	
	# flags for C and C++
	env['CCFLAGS'] = [
		'$CCFLAGS_target',
		'$CCFLAGS_optimize',
		'$CCFLAGS_debug',
		'$CCFLAGS_warning',
		'$CCFLAGS_other'
	]
	
	env['CCFLAGS_target'] = ['-mcpu=v8', '-msoft-float',]
	env['CCFLAGS_optimize'] = ['-O2', '-ffunction-sections', '-fdata-sections',]
	env['CCFLAGS_debug'] = ['-g']
	env['CCFLAGS_warning'] = [
		'-W',
		'-Wall',
		'-Wextra',
		'-Wformat',
		'-Wunused-parameter',
		'-Wundef',
		'-Winit-self',
		'-Wcast-qual',
		'-Wcast-align',
		'-Wpointer-arith',
		'-Wwrite-strings',
		'-Wmissing-declarations',
		'-Wredundant-decls',
		'-Wunused',
		'-Winline',
		'-Wuninitialized',
#		'-Wshadow',
#		'-Wconversion',
	]
	
	# only after for gcc >= 4.6
	if compiler_version >= 40600:
		env['CCFLAGS_warning'].append('-Wdouble-promotion')
	
	env['CCFLAGS_other'] = []
	
	# C flags
	env['CFLAGS'] = [
		'$CFLAGS_language',
		'$CFLAGS_warning',
	]
	
	env['CFLAGS_language'] = [
		'-std=c99',
		'-pedantic',
	]
	env['CFLAGS_warning'] = [
		'-Wimplicit',
		'-Wstrict-prototypes',
		'-Wredundant-decls',
		'-Wnested-externs',
	]
	
	# C++ flags
	env['CXXFLAGS'] = [
		'$CXXFLAGS_language',
		'$CXXFLAGS_warning',
		'$CXXFLAGS_other',
	]
	
	env['CXXFLAGS_language'] = [
		'-std=c++98',
		'-pedantic',
		'-fno-rtti',
		'-fno-exceptions',
	]
	
	env['CXXFLAGS_warning'] = [
		'-Wold-style-cast',
		'-Woverloaded-virtual',
		'-Wnon-virtual-dtor',
	]
	
	env['LINKFLAGS'] = [
		'$CCFLAGS',
		'--gc-sections',
	]

# -----------------------------------------------------------------------------	
def exists(env):
	return env.Detect('gcc')
	