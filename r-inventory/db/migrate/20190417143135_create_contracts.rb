class CreateContracts < ActiveRecord::Migration[5.2]
  def change
    create_table :contracts do |t|
      t.string :number
      t.date :end_of_contract
      t.string :provider

      t.timestamps
    end
  end
end
