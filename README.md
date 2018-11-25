# Minetest Mod Profiler

**Time measurement tool for Mod developers**

![profiler](https://github.com/joe7575/profiler/blob/master/screenshot.png)


Browse on: ![GitHub](https://github.com/joe7575/profiler)

Download: ![GitHub](https://github.com/joe7575/profiler/archive/master.zip)


## Introduction
The necessary steps to measure your Mod performance:
1. **Make a backup of your mod code (to be on the safer side)**
2. Take care that your mod is prepared for profiling (see below)
3. Switch to the profiler folder
4. Instrument your code by means of ``python ./profiler.py instrument ../mymod``
5. Start your Minetest server: ``./minetestserver  --worldname myworld``
6. Start your Minetest client, connect to the server and teleport to the location where your mod works
7. Start profiling by means of the ingame command ``/profiler_start``
8. Wait a few minutes
9. Stop profiling by means of the ingame command ``/profiler_stop``
10. De-instrument your code: ``python ./profiler.py de-instrument ../mymod``
11. Load the CSV file from your world folder in your spreadsheet application (Excel, Calc, ...)


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


## Hints for good measurement results
For the measurements before/after the modification/optimization, try to produce the same conditions, like:
* Try to run the Minetest server on a dedicated computer, isolated from the Minitest client
* Minimize the number of running applications on your server
* Always use the same computer, the same activated mods, the same game engine, and so on
* Place your avatar always at the same position
* Take care that your mod operates the same


## Dependencies
none  


# License
Copyright (C) 2018 Joachim Stolberg  
Licensed under the GNU LGPL version 2.1 or later.  
See LICENSE.txt and http://www.gnu.org/licenses/lgpl-2.1.txt  
