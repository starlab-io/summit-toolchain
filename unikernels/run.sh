#!/bin/bash

IP=192.168.1.134


sudo xl destroy crash-kernel

rumprun -S xen -d -M 16 -N crash-kernel \
	-I xen0,xenif \
	-W xen0,inet,static,$IP/24 \
	./crash_kernel.run
