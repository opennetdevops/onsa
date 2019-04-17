class CreateBackboneNodes < ActiveRecord::Migration[5.2]
  def change
    create_table :backbone_nodes do |t|
      t.string :hostname
      t.cidr :mgmt_ip
      t.integer :location_id
      t.cidr :loopback
      t.integer :device_model_id
      t.string :serial_number
      t.string :firmware_version
      t.string :ot
      t.date :intallation_date
      t.string :config_status
      t.string :comments
      t.integer :contract_id

      t.timestamps
    end
  end
end
