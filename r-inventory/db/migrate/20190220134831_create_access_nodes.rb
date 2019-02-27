class CreateAccessNodes < ActiveRecord::Migration[5.2]
  def change
    create_table :access_nodes do |t|
      t.string :name
      t.cidr :mgmt_ip
      t.string :model
      t.string :vendor
      t.integer :location_id
      t.string :uplink_interface
      t.string :uplink_ports
      t.integer :provider_vlan
      t.integer :logical_unit_id

      t.timestamps
    end
  end
end
