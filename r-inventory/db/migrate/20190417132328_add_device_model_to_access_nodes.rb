class AddDeviceModelToAccessNodes < ActiveRecord::Migration[5.2]
  def change
    add_column :access_nodes, :device_model_id, :integer
  end
end
