class CreateVlans < ActiveRecord::Migration[5.2]
  def change
    create_table :vlans do |t|
      t.integer :vlan_tag
      t.timestamps
    end
  end
end
