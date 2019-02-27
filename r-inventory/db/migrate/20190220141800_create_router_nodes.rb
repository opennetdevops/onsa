class CreateRouterNodes < ActiveRecord::Migration[5.2]
  def change
    create_table :router_nodes do |t|
      t.string :name
      t.cidr :mgmt_ip
      t.string :model
      t.string :vendor
      t.integer :location_id
      t.cidr :private_wan_ip
      t.cidr :loopback

      t.timestamps
    end
  end
end
