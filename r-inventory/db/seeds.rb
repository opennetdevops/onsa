# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
files = Dir["db/seeds/local/*.json"]
files.each do |a|
    json = ActiveSupport::JSON.decode(File.read(a))
    file_name = File.basename(a, ".*")
    json.each do |b|
        c = Object.const_get(file_name.singularize.camelcase).new(b)
        c.save(validate: false)
    end
end

DeviceModel.create(brand:"Transition Networks Inc",model:"S4224")
DeviceModel.create(brand:"Transition Networks Inc",model:"SM24-100SFP-AH")
DeviceModel.create(brand:"Transition Networks Inc",model:"SM24-1000SFP-AH")
DeviceModel.create(brand:"Transition Networks Inc",model:"MRV OA2000")
DeviceModel.create(brand:"Transition Networks Inc",model:"MIL-SM4004TG")
DeviceModel.create(brand:"Net2Edge",model:"LIB4424")
DeviceModel.create(brand:"Juniper Networks",model:"EX4550")
DeviceModel.create(brand:"Juniper Networks",model:"MX104")
