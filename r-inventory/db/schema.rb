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

ActiveRecord::Schema.define(version: 2019_04_17_190952) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "access_nodes", force: :cascade do |t|
    t.string "hostname"
    t.cidr "mgmt_ip"
    t.integer "location_id"
    t.string "remote_ports"
    t.string "uplink_ports"
    t.integer "provider_vlan"
    t.integer "logical_unit_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "device_model_id"
    t.string "serial_number"
    t.string "firmware_version"
    t.string "ot"
    t.string "comments"
    t.string "config_status"
    t.integer "contract_id"
    t.date "installation_date"
    t.bigint "remote_device_id"
    t.index ["remote_device_id"], name: "index_access_nodes_on_remote_device_id"
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

  create_table "active_admin_comments", force: :cascade do |t|
    t.string "namespace"
    t.text "body"
    t.string "resource_type"
    t.bigint "resource_id"
    t.string "author_type"
    t.bigint "author_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["author_type", "author_id"], name: "index_active_admin_comments_on_author_type_and_author_id"
    t.index ["namespace"], name: "index_active_admin_comments_on_namespace"
    t.index ["resource_type", "resource_id"], name: "index_active_admin_comments_on_resource_type_and_resource_id"
  end

  create_table "admin_users", force: :cascade do |t|
    t.string "email", default: "", null: false
    t.string "encrypted_password", default: "", null: false
    t.string "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.integer "sign_in_count", default: 0, null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.inet "current_sign_in_ip"
    t.inet "last_sign_in_ip"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["email"], name: "index_admin_users_on_email", unique: true
    t.index ["reset_password_token"], name: "index_admin_users_on_reset_password_token", unique: true
  end

  create_table "backbone_nodes", force: :cascade do |t|
    t.string "hostname"
    t.cidr "mgmt_ip"
    t.integer "location_id"
    t.cidr "loopback"
    t.integer "device_model_id"
    t.string "serial_number"
    t.string "firmware_version"
    t.string "ot"
    t.date "intallation_date"
    t.string "config_status"
    t.string "comments"
    t.integer "contract_id"
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
    t.string "client"
    t.string "uplink_port"
    t.string "customer_location"
    t.integer "location_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "device_model_id"
  end

  create_table "contracts", force: :cascade do |t|
    t.string "number"
    t.date "end_of_contract"
    t.string "provider"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "device_models", force: :cascade do |t|
    t.string "brand"
    t.string "model"
    t.date "end_of_life"
    t.date "end_of_support"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "distribution_nodes", force: :cascade do |t|
    t.string "hostname"
    t.cidr "mgmt_ip"
    t.integer "location_id"
    t.string "remote_ports"
    t.string "uplink_ports"
    t.integer "device_model_id"
    t.string "serial_number"
    t.string "firmware_version"
    t.string "ot"
    t.string "comments"
    t.string "config_status"
    t.integer "contract_id"
    t.date "installation_date"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "remote_device_id"
    t.index ["remote_device_id"], name: "index_distribution_nodes_on_remote_device_id"
  end

  create_table "locations", force: :cascade do |t|
    t.string "name"
    t.string "address"
    t.string "pop_size"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.string "region"
    t.string "shortname"
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
    t.string "hostname"
    t.cidr "mgmt_ip"
    t.integer "location_id"
    t.cidr "private_wan_ip"
    t.cidr "loopback"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.integer "device_model_id"
    t.string "serial_number"
    t.string "firmware_version"
    t.string "ot"
    t.date "installation_date"
    t.string "config_status"
    t.string "comments"
    t.integer "contract_id"
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

  add_foreign_key "access_nodes", "distribution_nodes", column: "remote_device_id"
  add_foreign_key "distribution_nodes", "router_nodes", column: "remote_device_id"
end
