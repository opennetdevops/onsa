from mongoengine import *

class AccessPorts(EmbeddedDocument):
	id = StringField(max_length=50, required=True, unique=True)

	def values(self):
		values = dict(self.to_mongo())
		return values