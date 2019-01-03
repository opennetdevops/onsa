const onsaServices = [{'id': 1, 'type': 'cpeless_irs'},
	                  {'id': 2, 'type': 'cpe_irs'},
	                  {'id': 3, 'type': 'cpeless_mpls'},
	                  {'id': 4, 'type': 'cpe_mpls'},
	                  {'id': 5, 'type': 'vpls'},
	                  {'id': 6, 'type': 'vcpe_irs'}];

const serviceEnum = {
  'cpeless_irs': 'CPEless IRS',
  'cpeless_mpls': 'CPEless MPLS',
  'cpe_irs': 'CPE IRS',
  'cpe_mpls': 'CPE MPLS',
  'vpls': 'VPLS',
  'vcpe_irs': 'vCPE'
}

const serviceStatesEnum = {
	'in_construction': 'IN CONSTRUCTION',
	'an_activation_in_progress': 'CONFIGURING ACCESS NODE',
	'bb_activation_in_progress': 'CONFIGURING ROUTER NODE',
	'an_activated': 'WAITING FOR BACKBONE CONFIGURATION',
	'bb_activated': 'WAITING FOR CPE ASIGNMENT',
	'cpe_data_ack': 'WAITING FOR CPE CONFIGURATION',
	'cpe_activation_in_progress': 'CONFIGURING CPE NODE',
	'bb_data_ack': 'WAITING FOR BACKBONE CONFIGURATION',
	'service_activated': 'SERVICE ACTIVATED',
}

const onsaVrfServices = ['cpe_mpls', 'cpeless_mpls', 'vpls'];

const onsaIrsServices = ['cpe_irs', 'cpeless_irs', 'vcpe_irs'];

export { onsaServices, onsaVrfServices, onsaIrsServices, serviceEnum, serviceStatesEnum };