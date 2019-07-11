const onsaServices = [
  { id: 1, type: "cpeless_irs" },
  { id: 2, type: "cpe_irs" },
  { id: 3, type: "cpeless_mpls" },
  { id: 4, type: "cpe_mpls" },
  { id: 5, type: "vpls" },
  { id: 6, type: "vcpe_irs" },
  { id: 7, type: "tip" }
];

const serviceEnum = {
  cpeless_irs: "CPEless IRS",
  cpeless_mpls: "CPEless MPLS",
  cpe_irs: "CPE IRS",
  cpe_mpls: "CPE MPLS",
  vpls: "VPLS",
  vcpe_irs: "vCPE",
  tip: "TIP"
};

const serviceStatesEnum = {
  in_construction: "IN CONSTRUCTION",
  an_activation_in_progress: "CONFIGURING ACCESS NODE",
  bb_activation_in_progress: "CONFIGURING ROUTER NODE",
  an_activated: "WAITING FOR BACKBONE CONFIGURATION",
  bb_activated: "WAITING FOR CPE ASIGNMENT",
  cpe_data_ack: "WAITING FOR CPE CONFIGURATION",
  cpe_activation_in_progress: "CONFIGURING CPE NODE",
  bb_data_ack: "WAITING FOR BACKBONE CONFIGURATION",
  service_activated: "SERVICE ACTIVATED",
  delete_in_progress: "DELETE IN PROGRESS",
  deleted: "DELETED",
  ERROR: "SERVICE ERROR",
  "ERROR IN DELETION": "ERROR WHILE DELETING CONFIG",
  AUTH_ERROR: "AUTHENTICATION ERROR",
  TIMEOUT_ERROR: "TIMEOUT ERROR",
  ROLLBACK_ERROR: "ROLLBACK ERROR"
};

const notDeletableStates = [
  "deleted",
  "an_activation_in_progress",
  "bb_activation_in_progress",
  "cpe_activation_in_progress",
  "delete_in_progress",
  "ERROR"
];

const retryableStates = [
  "ERROR",
  "AUTH_ERROR",
  "TIMEOUT_ERROR",
  "ROLLBACK_ERROR"
];

const resultantStates = [
  "an_activated",
  "bb_activated",
  "cpe_data_ack",
  "bb_data_ack",
  "service_activated",
  "deleted",
  "ERROR",
  "ERROR IN DELETION",
  "AUTH_ERROR",
  "TIMEOUT_ERROR",
  "ROLLBACK_ERROR"
];

const onsaVrfServices = ["cpe_mpls", "cpeless_mpls", "vpls"];

const onsaIrsServices = ["cpe_irs", "cpeless_irs", "vcpe_irs"];

const onsaExternalVlanServices = ["tip"];

export {
  onsaServices,
  onsaVrfServices,
  onsaIrsServices,
  serviceEnum,
  serviceStatesEnum,
  onsaExternalVlanServices,
  notDeletableStates,
  retryableStates,
  resultantStates
};
