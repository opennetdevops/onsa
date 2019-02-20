class CreateVlanTags < ActiveRecord::Migration[5.2]
  def change
    create_table :vlan_tags do |t|
      t.integer :vlan_tag

      t.timestamps
    end
  end
end
