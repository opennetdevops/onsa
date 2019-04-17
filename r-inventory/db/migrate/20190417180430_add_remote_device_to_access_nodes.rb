class AddRemoteDeviceToAccessNodes < ActiveRecord::Migration[5.2]
  def change
  	remove_column :access_nodes, :remote_device, :integer
  	add_reference(:access_nodes, :remote_device, foreign_key: {to_table: :distribution_nodes})
  end
end
