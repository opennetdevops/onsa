class RemoveAttrsFromAccessNodes < ActiveRecord::Migration[5.2]
  def change
    remove_column :access_nodes, :vendor, :string
    remove_column :access_nodes, :model, :string
  end
end
