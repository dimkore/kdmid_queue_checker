import time
import os
import argparse 

from core.queue_checker import QueueChecker

# kdmid_subdomain = 'madrid' 
# order_id = '130238' 
# code = 'CD9E05C1' 

# https://warsaw.kdmid.ru/queue/OrderInfo.aspx?id=85914&cd=824D737D

kdmid_subdomain = 'warsaw'
order_id = '85914'
code = '824D737D'

def run(queue_checker, every_hours): 
	success = False
	while not success:
	    if not os.path.isfile(queue_checker.order_id+"_"+queue_checker.code+"_success.json"):
	        queue_checker.check_queue(kdmid_subdomain, order_id, code)
	        time.sleep(every_hours*3600)
	    else: 
	        print('file exists, exiting')
	        success = True

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Parameters for checking')

	parser.add_argument('--subdomain',
	                       type=str, required=True,
	                       help='The city where the consulate is situated')
 	
	parser.add_argument('--order_id',
	                       type=str, required=True,
	                       help='Номер заявки')
 	
	parser.add_argument('--code',
	                       type=str, required=True,
	                       help='Защитный код')
 	
	parser.add_argument('--every_hours',
	                       type=int, default=3,
	                       help='Every n hours to check the queue, default 3')

	args = parser.parse_args()

	kdmid_subdomain, order_id, code = args.subdomain, args.order_id, args.code

	queue_checker = QueueChecker()

	run(queue_checker, args.every_hours)
