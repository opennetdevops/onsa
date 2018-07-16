import jinja2
from .edge import *

def render(tpl_path, context):
	path, filename = os.path.split(tpl_path)

	return jinja2.Environment(
		loader=jinja2.FileSystemLoader(path or './')
	).get_template(filename).render(context)

class NsxHandler(object):

	def create_edge(params):
		return nsx_edge_create(params)

	def add_gateway(edge_name):
		edge_id = nsx_edge_get_id_by_name(edge_name)
		return nsx_edge_add_gateway(edge_id, "0", "100.64.4.1", "1500")
	



