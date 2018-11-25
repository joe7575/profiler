local function my_timer_func(pos, elapsed)
	-- so something
end

minetest.register_node("mymode:mynode", {
	description = "blub",
	drawtype = "glasslike",
	tiles = { "test.png" },
	
	on_timer = my_timer_func,

	paramtype = "light",
	light_source = 0,	
	sunlight_propagates = true,
	paramtype2 = "facedir",
	groups = {cracky=2, crumbly=2, choppy=2},
	is_ground_content = false,
})
