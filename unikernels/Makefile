##
## STAR LAB PROPRIETARY & CONFIDENTIAL
## Copyright (C) 2016, Star Lab — All Rights Reserved
## Unauthorized copying of this file, via any medium is strictly prohibited.
##

CC = x86_64-rumprun-netbsd-gcc 
#CFLAGS = -std=gnu99 -Wall -Wno-missing-braces
#CFLAGS += -ggdb

#MWROOT  = ../../../..

#CFLAGS += -I..
#CFLAGS += -I$(MWROOT)/common
#CFLAGS += -I$(MWROOT)/exports/imports
#CFLAGS += -I../platform/xen/xen/include 
#CFLAGS += -I../../rump-common




BAKE=rumprun-bake
BAKE_FLAGS=xen_pv

# For testing without /dev/xe
#BAKE_FLAGS=xen_pv

# For testing outside of Rump, use Makefile.util

APPNAME=crash_kernel


ARCHIVES=

all: $(APPNAME).run

# We can call rumprun-bake in the most annoying manner possible;
# but it shows exactly what the bake script is doing. Here's how:
# bash -x `which $(BAKE)` $(BAKE_FLAGS) $@ $^ $(ARCHIVES)	
#
# Direct running instrutions:
#@echo "Run    rumprun -S xen -i $@"
#@echo " rumprun -S xen -dip -D 1234 $@"
#
# N.B. Calling rumprun with -d works here, but it doesn't work with
# thread_app. Why?

$(APPNAME).run: $(APPNAME).bin
	$(BAKE) $(BAKE_FLAGS) $@ $^ $(ARCHIVES)
	@echo "Run   ./run.sh"
	@echo "Or debug with ./debug.sh and"
	@echo " gdb -ex 'target remote localhost:1234' $@"

$(APPNAME).bin: crash_kernel.c
	$(CC) $(CFLAGS) -o $@ $^


clean:
	rm -f $(APPNAME).run $(APPNAME).bin *.o
