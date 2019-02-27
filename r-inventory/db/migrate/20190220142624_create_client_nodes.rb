class CreateClientNodes < ActiveRecord::Migration[5.2]
  def change
    create_table :client_nodes, id: false do |t|
      t.string :name
      t.cidr :mgmt_ip
      t.string :model
      t.string :vendor
      t.string :serial_number,primary_key: true
      t.string :client
      t.string :uplink_port
      t.string :customer_location
      t.integer :location_id
      t.timestamps
    end
  end
end
