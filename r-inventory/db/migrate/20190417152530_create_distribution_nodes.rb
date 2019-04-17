class CreateDistributionNodes < ActiveRecord::Migration[5.2]
  def change
    create_table :distribution_nodes do |t|
      t.string :hostname
      t.cidr :mgmt_ip
      t.integer :location_id
      t.string :remote_ports
      t.string :uplink_ports
      t.integer :device_model_id
      t.string :serial_number
      t.string :firmware_version
      t.string :ot
      t.string :comments
      t.string :config_status
      t.integer :contract_id
      t.date :installation_date
      t.integer :remote_device

      t.timestamps
    end
  end
end
