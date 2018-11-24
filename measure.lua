-------------------------------------------------------------------------------
-- Profiler
-------------------------------------------------------------------------------

-- To filter out thread changes 
local MAX_VALUE = 1000  -- 1 ms

local tData = {}

local start = nil

function profiler.profile(id, func, pos, elapsed)
	local t = minetest.get_us_time()
	local res = func(pos, elapsed)
	if start then
		t = minetest.get_us_time() - t
		if t < MAX_VALUE then
			if not tData[id] then
				tData[id] = {time = 0, calls = 0, tmax = 0}
			end
			tData[id].time = tData[id].time + t
			tData[id].tmax = math.max(tData[id].tmax, t)
			tData[id].calls = tData[id].calls + 1
		end
	end
	return res
end

local function store_data()
	local f = io.open(minetest.get_worldpath()..DIR_DELIM.."profiling.csv", "w")
	f:write("function,calls,sum/us,max/us,avg/us\n")
	for id,item in pairs(tData) do
		local ref = profiler.lReferences[id]
		local avg = math.floor(item.time / item.calls)
		f:write(ref..","..item.calls..","..item.time..","..item.tmax..","..avg.."\n")
	end
	f:write("measurement time,"..(minetest.get_us_time() - start).."\n")
	f:close()
end

minetest.register_chatcommand("profiler_start", {
	description = "Store profiling data to file",
	privs = {server=true},
	func = function(name, param)
		tData = {}
		start = minetest.get_us_time()
		return true, "Profiler started"
	end
})

minetest.register_chatcommand("profiler_stop", {
	description = "Store profiling data to file",
	privs = {server=true},
	func = function(name, param)
		store_data()
		return true, "Profiling data stored"
	end
})

