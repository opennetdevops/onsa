class RenameFieldRouterNodes < ActiveRecord::Migration[5.2]
  def change
  	rename_column :router_nodes, :name, :hostname
  end
end
