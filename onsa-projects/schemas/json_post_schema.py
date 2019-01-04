json_post_schema = {
	'type': 'object',
	'properties': {
		'svc_id': {'type': 'string'},
		'bandwidth': {'type': 'number'},
	},
	'required': ['svc_id', 'bandwidth']
}