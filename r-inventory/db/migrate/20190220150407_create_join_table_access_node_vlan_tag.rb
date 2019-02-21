class CreateJoinTableAccessNodeVlanTag < ActiveRecord::Migration[5.2]
  def change
    create_join_table :access_nodes, :vlan_tags do |t|
      # t.index [:access_node_id, :vlan_tag_id]
      # t.index [:vlan_tag_id, :access_node_id]
    end
  end
end
