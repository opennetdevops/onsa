class CreateLogicalUnits < ActiveRecord::Migration[5.2]
  def change
    create_table :logical_units do |t|

      t.timestamps
    end
  end
end
