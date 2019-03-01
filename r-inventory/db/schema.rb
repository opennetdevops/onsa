# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2019_02_20_150407) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "access_nodes", force: :cascade do |t|
    t.string "name"
    t.cidr "mgmt_ip"
    t.string "model"
    t.string "vendor"
    t.integer "location_id"
    t.string "uplink_interface"
    t.string "uplink_ports"
    t.integer "provider_vlan"
    t.integer "logical_unit_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "access_nodes_vlans", id: false, force: :cascade do |t|
    t.bigint "access_node_id", null: false
    t.bigint "vlan_id", null: false
  end

  create_table "access_ports", force: :cascade do |t|
    t.string "port"
    t.boolean "used"
    t.integer "access_node_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "client_node_ports", force: :cascade do |t|
    t.string "interface_name"
    t.string "client_node_id"
    t.boolean "used"
    t.string "service_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "client_nodes", primary_key: "serial_number", id: :string, force: :cascade do |t|
    t.string "name"
    t.cidr "mgmt_ip"
    t.string "model"
    t.string "vendor"
    t.string "client"
    t.string "uplink_port"
    t.string "customer_location"
    t.integer "location_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "locations", force: :cascade do |t|
    t.string "name"
    t.string "address"
    t.string "pop_size"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "locations_vrfs", id: false, force: :cascade do |t|
    t.bigint "location_id", null: false
    t.bigint "vrf_id", null: false
  end

  create_table "logical_units", force: :cascade do |t|
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "logical_units_router_nodes", id: false, force: :cascade do |t|
    t.bigint "router_node_id", null: false
    t.bigint "logical_unit_id", null: false
  end

  create_table "router_nodes", force: :cascade do |t|
    t.string "name"
    t.cidr "mgmt_ip"
    t.string "model"
    t.string "vendor"
    t.integer "location_id"
    t.cidr "private_wan_ip"
    t.cidr "loopback"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "vlans", force: :cascade do |t|
    t.integer "vlan_tag"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "vrfs", force: :cascade do |t|
    t.string "rt"
    t.string "name"
    t.boolean "used"
    t.string "description"
    t.string "client"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

end
