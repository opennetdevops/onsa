from mongoengine import *
from models.AccessPorts import AccessPorts
from models.Vrfs import Vrfs
from models.Locations import Locations

class Projects(Document):
	svc_id = StringField(max_length=50, required=True, unique=True)
	bandwidth = IntField()
	access_ports = EmbeddedDocumentListField(AccessPorts)
	locations = EmbeddedDocumentListField(Locations)
	vrfs = EmbeddedDocumentListField(Vrfs)

	def values(self):
		values = dict(self.to_mongo())
		values.pop("_id")
		return values

	def add_access_ports(self, ports):
		for port in ports:
			self.access_ports.append(AccessPorts(id=port['id']))

	def find_access_port(self, id):
		for port in self.access_ports:
			if port.id == id:
				return port

	def insert_access_port(self, id):
		self.update(push__access_ports={"id": id})

	def delete_access_port(self, id):
		self.update(pull__access_ports={"id": id})

	def add_locations(self, locs):
		for loc in locs:
			self.locations.append(Locations(id=loc['id'], logical_units=loc['logical_units']))

	def delete_logical_unit(self, loc_id, id):
		Projects.objects(locations__id=id).update(pull__locations__S__logical_units={"id": id})

	def add_vrfs(self, vrfs):
		for vrf in vrfs:
			self.vrfs.append(Vrfs(id=vrf['id']))

	def find_vrf(self, id):
		for vrf in self.vrfs:
			if vrf.id == id:
				return vrf

	def insert_vrf(self, id):
		self.update(push__vrfs={"id": id})

	def delete_vrf(self, id):
		self.update(pull__vrfs={"id": id})