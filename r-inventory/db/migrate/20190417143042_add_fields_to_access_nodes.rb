class AddFieldsToAccessNodes < ActiveRecord::Migration[5.2]
  def change
    add_column :access_nodes, :serial_number, :string
    add_column :access_nodes, :firmware_version, :string
    add_column :access_nodes, :ot, :string
    add_column :access_nodes, :comments, :string
    add_column :access_nodes, :config_status, :string
    add_column :access_nodes, :contract_id, :integer
  end
end
