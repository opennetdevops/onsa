class AddMulticlientPortToAccessPorts < ActiveRecord::Migration[5.2]
  def change
    add_column :access_ports, :multiclient_port, :boolean
  end
end
