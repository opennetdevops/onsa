from mongoengine import *
from models.LogicalUnits import LogicalUnits

class Locations(EmbeddedDocument):
	id = StringField(max_length=50, required=True, unique=True)
	logical_units = EmbeddedDocumentListField(LogicalUnits)

	def values(self):
		values = dict(self.to_mongo())
		return values