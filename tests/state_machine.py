from transitions import Machine

INIT_STATE = 'access'

class vCPETaskMachine(object):
	def __init__(self):
		self.task_state = False

	def run_task(self, devices):
		for device in devices:
			if device['model'] == self.state:
				task = 1
				self.task_state = True
				print(self.state)

	def rollback(self): print("Rollback!")

states = ['mx104', 'nsx', 'access', 'rollback']

transitions = [
	{ 'trigger': 'success', 'source': '*', 'dest': '*'},
    { 'trigger': 'failed', 'source': '*', 'dest': 'rollback'}
]

taskMachine = vCPETaskMachine()
machine = Machine(taskMachine, states=states, initial=INIT_STATE)

taskMachine.init(devices=[{'model' : 'mx104'}])
taskMachinetaskMachine.success(devices=[{'model' : 'nsx'}])
taskMachine.success(devices=[{'model' : 'access'}])
taskMachineq.failed()
