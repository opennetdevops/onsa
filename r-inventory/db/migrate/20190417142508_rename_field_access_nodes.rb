class RenameFieldAccessNodes < ActiveRecord::Migration[5.2]
  def change
  	rename_column :access_nodes, :name, :hostname
  end
end
