class RemoveFieldsFromRouterNodes < ActiveRecord::Migration[5.2]
  def change
    remove_column :router_nodes, :model, :string
    remove_column :router_nodes, :vendor, :string
  end
end
