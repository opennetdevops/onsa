class CreateAccessPorts < ActiveRecord::Migration[5.2]
  def change
    create_table :access_ports do |t|
      t.string :port
      t.boolean :used
      t.integer :access_node_id

      t.timestamps
    end
  end
end
