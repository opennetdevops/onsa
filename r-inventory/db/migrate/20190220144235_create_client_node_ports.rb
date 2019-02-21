class CreateClientNodePorts < ActiveRecord::Migration[5.2]
  def change
    create_table :client_node_ports do |t|
      t.string :interface_name
      t.integer :client_node_id
      t.boolean :used
      t.string :service_id

      t.timestamps
    end
  end
end
