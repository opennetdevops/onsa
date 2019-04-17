class AddDeviceModelToClientNodes < ActiveRecord::Migration[5.2]
  def change
    add_column :client_nodes, :device_model_id, :integer
  end
end
