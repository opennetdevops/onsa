class GreetMe:
	def __init__(self,name):
		self.name = name

	def __getattr__(self, attr):

		allowed = ['hello', 'bye', 'good_bye']

		def call_(name=None):
			if attr in allowed:
				greeting = attr.replace('_', '')
				print(greeting)
				target = name if name else self.name
				print(target)

				return target, greeting.capitalize()
			else:
				raise ValueError("Invalid name or greeting")

		return call_

greet = GreetMe('Archi')

target, _ = greet.hello()

print(target)