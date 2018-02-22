# Server Mapping

# AbrAlgo: {0: 'Default', 1: 'Fixed Rate (0)', 2: 'Buffer Based', 3: 'Rate Based', 4: 'RL', 5: 'Festive', 6: 'Bola'}

# 0		Default		Default Algorithm			?										http://localhost:8111/
# 1		FIXED		Fixed Rate					http://localhost/myindex_FIXED.html 	http://localhost:8222/ (default case)
# 2		BB			Buffer Based				http://localhost/myindex_BB.html 		http://localhost:8333/
# 3		RB			Rate Based					http://localhost/myindex_RB.html 		http://localhost:8444/
# 4		RL			Pensieve					http://localhost/myindex_RL.html 		http://localhost:8555/
# 4		FastMPC		Precomputed MPC				http://localhost/myindex_fastMPC.html 	http://localhost:8666/
# 4		RobustMPC	MPC							http://localhost/myindex_robustMPC.html http://localhost:8777/
# 4		newdash		?							http://localhost/myindex_newdash.html 	http://localhost:8888/
# 5		FESTIVE		Fair, Efficient, and		http://localhost/myindex_FESTIVE.html 	http://localhost:8999/
#					Stable adapTIVE algorithm
# 6		BOLA		Lyapunov Optimization		http://localhost/myindex_BOLA.html 		http://localhost:9111/

#!/bin/bash

/usr/bin/python -u ../rl_server/mpc_server.py & echo "MPC Server started with PID: "$!
sleep 5

/usr/bin/python -u ../rl_server/robust_mpc_server.py & echo "Robust MPC Server started with PID: "$!
sleep 5

/usr/bin/python -u ../rl_server/dash_server_original.py & echo "DASH Server Original started with PID: "$!
sleep 5

/usr/bin/python -u ../rl_server/simple_server.py & echo "Simple Server started with PID: "$!
sleep 5

/usr/bin/python -u ../rl_server/rl_server_no_training.py & echo "RL Pretrained Server started with PID: "$!
sleep 5
