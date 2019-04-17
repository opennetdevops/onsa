class AddFieldsToRouterNodes < ActiveRecord::Migration[5.2]
  def change
    add_column :router_nodes, :device_model_id, :integer
    add_column :router_nodes, :serial_number, :string
    add_column :router_nodes, :firmware_version, :string
    add_column :router_nodes, :ot, :string
    add_column :router_nodes, :installation_date, :date
    add_column :router_nodes, :config_status, :string
    add_column :router_nodes, :comments, :string
    add_column :router_nodes, :contract_id, :integer
  end
end
