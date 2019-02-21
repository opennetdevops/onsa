class CreateVrfs < ActiveRecord::Migration[5.2]
  def change
    create_table :vrfs do |t|
      t.string :rt
      t.string :name
      t.boolean :used
      t.string :description
      t.string :client

      t.timestamps
    end
  end
end
