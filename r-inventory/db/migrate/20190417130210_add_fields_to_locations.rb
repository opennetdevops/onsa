class AddFieldsToLocations < ActiveRecord::Migration[5.2]
  def change
    add_column :locations, :region, :string
    add_column :locations, :shortname, :string
  end
end
