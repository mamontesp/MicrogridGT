import gambit
g = gambit.Game.new_table([2,2])
g.title = "A prisoner's dilemma game"
g.players[0].label = "Alphonse"
g.players[1].label = "Gaston"
g.players[0].strategies[0].label = "Cooperate"
g.players[0].strategies[0].label = "Defect"
g[0,0][0] = 8
g[0,0][1] = 8
g[0,1][0] = 2
g[0,1][1] = 10
g[1,0][0] = 10
g[1,1][0] = 2
g[1,0][1] = 2
g[1,1][0] = 5
g[1,1][1] = 5

solver = gambit.nash.lcp_solve(g, use_strategic = True)
print solver