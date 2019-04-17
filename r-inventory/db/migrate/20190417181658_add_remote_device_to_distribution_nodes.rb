class AddRemoteDeviceToDistributionNodes < ActiveRecord::Migration[5.2]
  def change
  	remove_column :distribution_nodes, :remote_device, :integer
  	add_reference(:distribution_nodes, :remote_device, foreign_key: {to_table: :router_nodes})
  end
end
