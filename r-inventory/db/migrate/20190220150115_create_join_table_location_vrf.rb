class CreateJoinTableLocationVrf < ActiveRecord::Migration[5.2]
  def change
    create_join_table :locations, :vrves do |t|
      # t.index [:location_id, :vrf_id]
      # t.index [:vrf_id, :location_id]
    end
  end
end
