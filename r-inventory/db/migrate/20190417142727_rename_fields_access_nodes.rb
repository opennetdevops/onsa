class RenameFieldsAccessNodes < ActiveRecord::Migration[5.2]
  def change
  	rename_column :access_nodes, :uplink_interface, :remote_ports
  end
end
