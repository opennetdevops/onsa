class AddInstallationDateToAccessNodes < ActiveRecord::Migration[5.2]
  def change
    add_column :access_nodes, :installation_date, :date
    add_column :access_nodes, :remote_device, :integer
  end
end
