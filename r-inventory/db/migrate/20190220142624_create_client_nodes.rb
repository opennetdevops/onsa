class CreateClientNodes < ActiveRecord::Migration[5.2]
  def change
    create_table :client_nodes do |t|
      t.string :name
      t.inet :mgmt_ip
      t.string :model
      t.string :vendor
      t.integer :location_id
      t.string :serial_number
      t.string :client
      t.string :uplink_port
      t.string :customer_location

      t.timestamps
    end
  end
end
