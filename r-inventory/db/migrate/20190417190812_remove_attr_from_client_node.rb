class RemoveAttrFromClientNode < ActiveRecord::Migration[5.2]
  def change
  	remove_column :client_nodes, :model, :string
    remove_column :client_nodes, :vendor, :string
  end
end
