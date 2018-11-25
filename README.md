# Minetest Mod Profiler

**Time measurement tool for Mod developers**

![profiler](https://github.com/joe7575/profiler/blob/master/screenshot.png)


Browse on: ![GitHub](https://github.com/joe7575/profiler)

Download: ![GitHub](https://github.com/joe7575/profiler/archive/master.zip)


## Introduction
The steps to measure your Mod performance:
1. Prepare your mod "on_timer" routines (see below)
2. Instrument your code by means of ``python ./profiler.py instrument ../mymod``
3. Start your Minetest server: ``./minetestserver  --worldname myworld``
4. Start your Minetest client, connect to the server and teleport to the location where your mod works
5. Start profiling by means of the command ``/profiler_start``
6. Wait a few minutes
7. Stop profiling by means of the command ``/profiler_stop``
8. De-instrument your code: ``python ./profiler.py de-instrument ../mymod``
9. Load the CSV file from the world folder in your spreadsheet application (Excel, Calc, ...)


## Prepare your Mod
Your "on_timer" routines have to be local functions like:

	local function my_timer_func(pos, elapsed)
		...
	end


	minetest.register_node("mymod:mynode", {
		...
		on_timer = my_timer_func,
	})

When you instrument your code, the, line ``on_timer = my_timer_func,`` will be replaced by
``on_timer = function(pos, elapsed) return profiler.profile(<id>, my_timer_func, pos, elapsed) end,``
and will be restored when you de-instrument your code.

In addition, the tool will add/remove the profiler dependency in 'depends.txt'.


## Dependencies
none  


# License
Copyright (C) 2018 Joachim Stolberg  
Licensed under the GNU LGPL version 2.1 or later.  
See LICENSE.txt and http://www.gnu.org/licenses/lgpl-2.1.txt  
