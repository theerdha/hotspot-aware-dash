import sys
import os
import signal
import subprocess
import numpy as np
from time import sleep
from util import master_log

RUN_SCRIPT = 'run_video.py'
RANDOM_SEED = 42
RUN_TIME = 320  # sec
MM_DELAY = 40   # millisec

def mlog(msg):
    master_log(pkg="run_traces.py", fnc="main()", msg=msg)

def main():
	
	trace_path = sys.argv[1]
	abr_algo = sys.argv[2]
	process_id = sys.argv[3]
	ip = sys.argv[4]
	
	mlog("Trace path: {}".format(trace_path))
	mlog("ABR Algorithm: {}".format(abr_algo))
	mlog("Process ID: {}".format(process_id))
	mlog("IP: {}".format(ip))

	sleep_vec = range(1, 10)  # random sleep second

	files = os.listdir(trace_path)
	count_max = len(files)

	for count, f in enumerate(files):

		while True:

			np.random.shuffle(sleep_vec)
			sleep_time = sleep_vec[int(process_id)]
			
			# start abr algorithm server
			trace_file = f
			if abr_algo == 'BB':
    				command = 'exec /usr/bin/python ../rl_server/simple_server_BB.py ' + abr_algo + ' ' + trace_file
			elif abr_algo == 'RB':
    				command = 'exec /usr/bin/python ../rl_server/simple_server_RB.py ' + abr_algo + ' ' + trace_file
			elif abr_algo == 'FIXED':
    				command = 'exec /usr/bin/python ../rl_server/simple_server_FIXED.py ' + abr_algo + ' ' + trace_file
			elif abr_algo == 'FESTIVE':
    				command = 'exec /usr/bin/python ../rl_server/simple_server_FESTIVE.py ' + abr_algo + ' ' + trace_file
			elif abr_algo == 'BOLA':
    				command = 'exec /usr/bin/python ../rl_server/simple_server_BOLA.py ' + abr_algo + ' ' + trace_file
			elif abr_algo == 'fastMPC':
    				command = 'exec /usr/bin/python ../rl_server/mpc_server.py ' + trace_file
			elif abr_algo == 'robustMPC':
    				command = 'exec /usr/bin/python ../rl_server/robust_mpc_server.py ' + trace_file
			elif abr_algo == 'RL':
    				command = 'exec /usr/bin/python ../rl_server/rl_server_no_training.py ' + trace_file
			else: # retained for backward compatibility
					command = 'exec /usr/bin/python ../rl_server/simple_server.py ' + abr_algo + ' ' + trace_file

			rl_server_proc = subprocess.Popen(command, stdout=subprocess.PIPE,
											  stderr=subprocess.PIPE, shell=True)
			mlog("Server command exec: {}".format(command))
			sleep(2)
			
			command_proc = 'mm-delay ' + str(MM_DELAY) + \
					  ' mm-link 12mbps ' + trace_path + f + ' ' + \
					  '/usr/bin/python ' + RUN_SCRIPT + ' ' + ip + ' ' + \
					  abr_algo + ' ' + str(RUN_TIME) + ' ' + \
					  process_id + ' ' + f + ' ' + str(sleep_time)
			proc = subprocess.Popen(command_proc,
					  stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
			mlog("mm-delay command exec: {} of {}: {}\n".format(count+1, count_max, command_proc))
			(out, err) = proc.communicate()

			if 'DONE!' in out:
				mlog("Process execution successful. Breaking...")
				# kill abr algorithm server
				try:
					rl_server_proc.send_signal(signal.SIGINT)
					mlog("Kill signal sent to rate server successfully.\n")
					#(srvout, srverr) = rl_server_proc.communicate()
					#mlog("Server output: {}\nServer error: {}".format(srvout, srverr))
					#mlog("Server returncode: {}\n".format(rl_server_proc.returncode))
				except:
					mlog("Sending kill signal FAILED.\n")
				break
			else:
    				mlog("Process execution FAILED.\nProcess out: {},\nProcess error: {}\n".format(out, err))
				with open('./chrome_retry_log', 'ab') as retry_log:
					retry_log.write(abr_algo + '_' + f + '\n')
					retry_log.write(out + '\n')
					retry_log.flush()

	mlog("\n")

if __name__ == '__main__':
	main()
