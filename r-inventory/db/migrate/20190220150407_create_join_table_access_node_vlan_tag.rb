class CreateJoinTableAccessNodeVlan < ActiveRecord::Migration[5.2]
  def change
    create_join_table :access_nodes, :vlans do |t|
    end
  end
end
