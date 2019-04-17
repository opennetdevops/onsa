class CreateDeviceModels < ActiveRecord::Migration[5.2]
  def change
    create_table :device_models do |t|
      t.string :brand
      t.string :model
      t.date :end_of_life
      t.date :end_of_support

      t.timestamps
    end
  end
end
