from transitions import Machine
import random

class Task(object):
	def __init__(self):
		self.task_state = False
	def run_task(self, output):
		print(output)
		self.task_state = True
	def rollback(self): print("Rollback!")


states = ['init', 'mx', 'nsx', 'access', 'rollback', 'end']

transitions = [
	{ 'trigger': 'init', 'source' : 'init', 'dest' : 'mx'},
    { 'trigger': 'success', 'source': 'mx', 'dest': 'nsx'},
    { 'trigger': 'success', 'source': 'nsx', 'dest': 'access'},
    { 'trigger': 'success', 'source': 'access', 'dest': 'end'},
    { 'trigger': 'failed', 'source': 'mx', 'dest': 'rollback'},
    { 'trigger': 'failed', 'source': 'nsx', 'dest': 'rollback'},
    { 'trigger': 'failed', 'source': 'access', 'dest': 'rollback'}
]

task = Task()
machine = Machine(task, states=states, transitions=transitions, initial='init')
machine.on_enter_mx('run_task')
machine.on_enter_nsx('run_task')
machine.on_enter_access('run_task')
machine.on_enter_rollback('rollback')

print(task.state)
task.init(output="ERLIN!")
print(task.state)
print(task.task_state)