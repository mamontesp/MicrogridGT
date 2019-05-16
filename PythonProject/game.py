import gambit

g = gambit.Game.new_table([1,1,1,1,1])
g.title = "A microgrid design"

g.players[0].label = "PV"
g.players[1].label = "WT"
g.players[2].label = "LD"
g.players[3].label = "BT"
g.players[4].label = "DE"

g.players[0].strategies[0].label = "PV_strategy"
g.players[1].strategies[0].label = "WT_strategy"
g.players[2].strategies[0].label = "LD_strategy"
g.players[3].strategies[0].label = "BT_strategy"
g.players[4].strategies[0].label = "DE_strategy"

def playGame(pv, wt, ld, bt, de):
	#g.players.add("PV")
	#g.players.add("WT")
	#g.players.add("LD")
	#g.players.add("BT")
	#g.players.add("DE")
	print ('playGame')
