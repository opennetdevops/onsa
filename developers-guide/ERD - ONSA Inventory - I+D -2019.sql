CREATE TABLE "access_nodes" (
  "id" varchar,
  "hostname" string,
  "mgmt_ip" cidr,
  "location_id" integer,
  "remote_ports" string,
  "uplink_ports" string,
  "provider_vlan" integer,
  "logical_unit_id" integer,
  "created_at" datetime,
  "updated_at" datetime,
  "device_model_id" integer,
  "serial_number" string,
  "firmware_version" string,
  "ot" string,
  "comments" string,
  "config_status" string,
  "contract_id" integer,
  "installation_date" date,
  "remote_device_id" bigint
);

CREATE TABLE "access_nodes_vlans" (
  "id" varchar,
  "access_node_id" bigint,
  "vlan_id" bigint
);

CREATE TABLE "access_ports" (
  "id" varchar,
  "port" string,
  "used" boolean,
  "access_node_id" integer,
  "created_at" datetime,
  "updated_at" datetime,
  "multiclient_port" boolean,
  "has_sfp" boolean,
  "status" string
);

CREATE TABLE "backbone_nodes" (
  "id" varchar,
  "hostname" string,
  "mgmt_ip" cidr,
  "location_id" integer,
  "loopback" cidr,
  "device_model_id" integer,
  "serial_number" string,
  "firmware_version" string,
  "ot" string,
  "intallation_date" date,
  "config_status" string,
  "comments" string,
  "contract_id" integer,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "client_node_ports" (
  "id" varchar,
  "interface_name" string,
  "client_node_id" string,
  "used" boolean,
  "service_id" string,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "client_nodes" (
  "id" varchar,
  "name" string,
  "mgmt_ip" cidr,
  "client" string,
  "uplink_port" string,
  "customer_location" string,
  "location_id" integer,
  "created_at" datetime,
  "updated_at" datetime,
  "device_model_id" integer
);

CREATE TABLE "contracts" (
  "id" varchar,
  "number" string,
  "end_of_contract" date,
  "provider" string,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "device_models" (
  "id" varchar,
  "brand" string,
  "model" string,
  "end_of_life" date,
  "end_of_support" date,
  "created_at" datetime,
  "updated_at" datetime,
  "uplink_ports" string
);

CREATE TABLE "distribution_nodes" (
  "id" varchar,
  "hostname" string,
  "mgmt_ip" cidr,
  "location_id" integer,
  "remote_ports" string,
  "uplink_ports" string,
  "device_model_id" integer,
  "serial_number" string,
  "firmware_version" string,
  "ot" string,
  "comments" string,
  "config_status" string,
  "contract_id" integer,
  "installation_date" date,
  "created_at" datetime,
  "updated_at" datetime,
  "remote_device_id" bigint
);

CREATE TABLE "locations" (
  "id" varchar,
  "name" string,
  "address" string,
  "pop_size" string,
  "created_at" datetime,
  "updated_at" datetime,
  "region" string,
  "shortname" string
);

CREATE TABLE "locations_vrfs" (
  "id" varchar,
  "location_id" bigint,
  "vrf_id" bigint
);

CREATE TABLE "logical_units" (
  "id" varchar,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "logical_units_router_nodes" (
  "id" varchar,
  "router_node_id" bigint,
  "logical_unit_id" bigint
);

CREATE TABLE "router_nodes" (
  "id" varchar,
  "hostname" string,
  "mgmt_ip" cidr,
  "location_id" integer,
  "private_wan_ip" cidr,
  "loopback" cidr,
  "created_at" datetime,
  "updated_at" datetime,
  "device_model_id" integer,
  "serial_number" string,
  "firmware_version" string,
  "ot" string,
  "installation_date" date,
  "config_status" string,
  "comments" string,
  "contract_id" integer
);

CREATE TABLE "vlans" (
  "id" varchar,
  "vlan_tag" integer,
  "created_at" datetime,
  "updated_at" datetime
);

CREATE TABLE "vrfs" (
  "id" varchar,
  "rt" string,
  "name" string,
  "used" boolean,
  "description" string,
  "client" string,
  "created_at" datetime,
  "updated_at" datetime
);

ALTER TABLE "access_nodes_vlans" ADD FOREIGN KEY ("access_node_id") REFERENCES "access_nodes" ("id");

ALTER TABLE "access_nodes_vlans" ADD FOREIGN KEY ("vlan_id") REFERENCES "vlans" ("id");

ALTER TABLE "access_nodes" ADD FOREIGN KEY ("remote_device_id") REFERENCES "distribution_nodes" ("id");

ALTER TABLE "access_ports" ADD FOREIGN KEY ("access_node_id") REFERENCES "access_nodes" ("id");

ALTER TABLE "backbone_nodes" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "client_nodes" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "access_nodes" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "distribution_nodes" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "router_nodes" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "distribution_nodes" ADD FOREIGN KEY ("remote_device_id") REFERENCES "router_nodes" ("id");

ALTER TABLE "client_node_ports" ADD FOREIGN KEY ("client_node_id") REFERENCES "client_nodes" ("id");

ALTER TABLE "locations_vrfs" ADD FOREIGN KEY ("location_id") REFERENCES "locations" ("id");

ALTER TABLE "locations_vrfs" ADD FOREIGN KEY ("vrf_id") REFERENCES "vrfs" ("id");

ALTER TABLE "logical_units_router_nodes" ADD FOREIGN KEY ("logical_unit_id") REFERENCES "logical_units" ("id");

ALTER TABLE "logical_units_router_nodes" ADD FOREIGN KEY ("router_node_id") REFERENCES "router_nodes" ("id");

ALTER TABLE "backbone_nodes" ADD FOREIGN KEY ("device_model_id") REFERENCES "device_models" ("id");

ALTER TABLE "backbone_nodes" ADD FOREIGN KEY ("contract_id") REFERENCES "contracts" ("id");

ALTER TABLE "client_nodes" ADD FOREIGN KEY ("device_model_id") REFERENCES "device_models" ("id");

ALTER TABLE "router_nodes" ADD FOREIGN KEY ("device_model_id") REFERENCES "device_models" ("id");

ALTER TABLE "router_nodes" ADD FOREIGN KEY ("contract_id") REFERENCES "contracts" ("id");

ALTER TABLE "distribution_nodes" ADD FOREIGN KEY ("device_model_id") REFERENCES "device_models" ("id");

ALTER TABLE "distribution_nodes" ADD FOREIGN KEY ("contract_id") REFERENCES "contracts" ("id");

ALTER TABLE "access_nodes" ADD FOREIGN KEY ("device_model_id") REFERENCES "device_models" ("id");

ALTER TABLE "access_nodes" ADD FOREIGN KEY ("contract_id") REFERENCES "contracts" ("id");