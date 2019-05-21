class AddUplinkPortsToDeviceModels < ActiveRecord::Migration[5.2]
  def change
    add_column :device_models, :uplink_ports, :string
  end
end
