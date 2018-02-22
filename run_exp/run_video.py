import os
import sys
import signal
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from pyvirtualdisplay import Display
from time import sleep
from util import master_log

# TO RUN: download https://pypi.python.org/packages/source/s/selenium/selenium-2.39.0.tar.gz
# run sudo apt-get install python-setuptools
# run sudo apt-get install xvfb
# after untar, run sudo python setup.py install
# follow directions here: https://pypi.python.org/pypi/PyVirtualDisplay to install pyvirtualdisplay

# For chrome, need chrome driver: https://code.google.com/p/selenium/wiki/ChromeDriver
# chromedriver variable should be path to the chromedriver
# the default location for firefox is /usr/bin/firefox and chrome binary is /usr/bin/google-chrome
# if they are at those locations, don't need to specify

def mlog(msg):
    master_log(pkg="run_video.py", fnc="none", msg=msg)

def timeout_handler(signum, frame):
	raise Exception("Timeout")

ip = sys.argv[1]
abr_algo = sys.argv[2]
run_time = int(sys.argv[3])
process_id = sys.argv[4]
trace_file = sys.argv[5]
sleep_time = sys.argv[6]

mlog("ABR Algorithm: {}".format(abr_algo))
mlog("Run Time: {}".format(run_time))
mlog("Process ID: {}".format(process_id))
mlog("Trace File: {}".format(trace_file))
mlog("Sleep Time: {}".format(sleep_time))

# prevent multiple process from being synchronized
sleep(int(sleep_time))
	
# generate url
url = 'http://' + ip + '/' + 'myindex_' + abr_algo + '.html'
mlog("Server URL: {}".format(url))

# timeout signal
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(run_time + 30)
	
try:
	# copy over the chrome user dir
	default_chrome_user_dir = '../abr_browser_dir/chrome_data_dir'
	chrome_user_dir = '/tmp/chrome_user_dir_id_' + process_id
	os.system('rm -r ' + chrome_user_dir)
	os.system('cp -r ' + default_chrome_user_dir + ' ' + chrome_user_dir)
	
	# start abr algorithm server
	#if abr_algo == 'RL':
	#	command = 'exec /usr/bin/python ../rl_server/rl_server_no_training.py ' + trace_file
	#elif abr_algo == 'fastMPC':
	#	command = 'exec /usr/bin/python ../rl_server/mpc_server.py ' + trace_file
	#elif abr_algo == 'robustMPC':
	#	command = 'exec /usr/bin/python ../rl_server/robust_mpc_server.py ' + trace_file
	#else:
	#	command = 'exec /usr/bin/python ../rl_server/simple_server.py ' + abr_algo + ' ' + trace_file

	#proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	#sleep(2)
	
	# to not display the page in browser
	display = Display(visible=0, size=(800,600))
	display.start()
	mlog("Started supressed display.")
	
	# initialize chrome driver
	options=Options()
	chrome_driver = '../abr_browser_dir/chromedriver'
	options.add_argument('--user-data-dir=' + chrome_user_dir)
	options.add_argument('--ignore-certificate-errors')
	driver=webdriver.Chrome(chrome_driver, chrome_options=options)
	
	# run chrome
	driver.set_page_load_timeout(10)
	driver.get(url)
	mlog("Video playback started.")

	sleep(run_time)
	
	driver.quit()
	display.stop()
	mlog("Stopped supressed display and Chrome driver.\n")

	# kill abr algorithm server
	# proc.send_signal(signal.SIGINT)
	# proc.kill()
	
	print 'DONE!'
	
except Exception as e:
	mlog("Exception: {}".format(e))
	try:
		mlog("Exception-1 Handler: Trying to stop supressed display.\n")
		display.stop()
		# pass
	except Exception as ex2:
		mlog("Exception-1: Exception again!\nException: {}\n".format(ex2))
	try:
		mlog("Exception-2 Handler: Trying to stop Chrome driver.\n")
		driver.quit()
	except Exception as ex3:
		mlog("Exception-2: Exception again!\nException: {}\n".format(ex3))
	# try:
	# 	proc.send_signal(signal.SIGINT)
	# except:
	# 	pass
	
	# print e	
