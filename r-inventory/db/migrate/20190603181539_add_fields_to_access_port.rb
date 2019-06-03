class AddFieldsToAccessPort < ActiveRecord::Migration[5.2]
  def change
    add_column :access_ports, :has_sfp, :boolean
    add_column :access_ports, :status, :string
  end
end
