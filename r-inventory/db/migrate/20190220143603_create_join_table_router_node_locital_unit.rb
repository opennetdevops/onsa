class CreateJoinTableRouterNodeLocitalUnit < ActiveRecord::Migration[5.2]
  def change
    create_join_table :router_nodes, :logical_units do |t|
      # t.index [:router_node_id, :logical_unit_id]
      # t.index [:logical_unit_id, :router_node_id]
    end
  end
end
