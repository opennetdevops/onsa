require 'csv'
csv_text = File.read(Rails.root.join('db','network-devices-2019-05-27.csv'), encoding: "utf-8")
csv = CSV.parse(csv_text, :headers => true, :encoding => "utf-8",:col_sep =>",")
csv.each do |row|
	if row['hostname']  =~ /RAC/i
		puts "Migrando:#{row['hostname']} en el hub:#{row['hub']}"
		hostname = row['hostname']
		mgmt_ip = row['ip_management']
		location_id = Location.where(shortname:row['hub']).first.id
		device_model_id = DeviceModel.where(model:row['model']).first.id
		serial_number = row['serial_number']
		firmware_version = row['firmware_version']
		ot = row['ot']
		installation_date = row['installation_date']
		config_status = row['config_status']
		comments = row['comments']
		RouterNode.create!(hostname:hostname,mgmt_ip:mgmt_ip,location_id:location_id,
			device_model_id:device_model_id,serial_number:serial_number,ot:ot,
			firmware_version:firmware_version, installation_date:installation_date,config_status:config_status,comments:comments)
	elsif row['hostname']  =~ /SAC/i
		puts "Migrando:#{row['hostname']} en el hub:#{row['hub']}"
		hostname = row['hostname']
		mgmt_ip = row['ip_management']
		location_id = Location.where(shortname:row['hub']).first.id
		remote_ports = row['remote_ports']
		uplink_ports = row['uplink_ports']
		remote_device_id = nil
		device_model_id = DeviceModel.where(model:row['model']).first.id
		serial_number = row['serial_number']
		firmware_version = row['firmware_version']
		ot = row['ot']
		installation_date = row['installation_date']
		config_status = row['config_status']
		comments = row['comments']
		DistributionNode.create!(hostname:hostname,mgmt_ip:mgmt_ip,location_id:location_id,
			remote_ports:remote_ports,uplink_ports:uplink_ports,remote_device_id:remote_device_id,
			device_model_id:device_model_id,serial_number:serial_number,ot:ot,
			firmware_version:firmware_version,installation_date:installation_date,config_status:config_status,comments:comments)
	elsif row['hostname']  =~ /SCO/i
		puts "Migrando:#{row['hostname']} en el hub:#{row['hub']}"
		hostname = row['hostname']
		mgmt_ip = row['ip_management']
		location_id = Location.where(shortname:row['hub']).first.id
		remote_ports = row['remote_ports']
		uplink_ports = row['uplink_ports']
		remote_device_id = nil
		device_model_id = DeviceModel.where(model:row['model']).first.id
		serial_number = row['serial_number']
		firmware_version = row['firmware_version']
		ot = row['ot']
		installation_date = row['installation_date']
		config_status = row['config_status']
		comments = row['comments']
		AccessNode.create!(hostname:hostname,mgmt_ip:mgmt_ip,location_id:location_id,
			remote_ports:remote_ports,uplink_ports:uplink_ports,remote_device_id:remote_device_id,
			device_model_id:device_model_id,serial_number:serial_number,ot:ot,
			firmware_version:firmware_version,installation_date:installation_date,config_status:config_status,comments:comments)
	else
		puts "Migrando:#{row['hostname']} en el hub:#{row['hub']}"
		hostname = row['hostname']
		mgmt_ip = row['ip_management']
		location_id = Location.where(shortname:row['hub']).first.id
		device_model_id = DeviceModel.where(model:row['model']).first.id
		serial_number = row['serial_number']
		firmware_version = row['firmware_version']
		ot = row['ot']
		installation_date = row['installation_date']
		config_status = row['config_status']
		comments = row['comments']
		BackboneNode.create!(hostname:hostname,mgmt_ip:mgmt_ip,location_id:location_id,device_model_id:device_model_id,
			serial_number:serial_number, ot:ot, intallation_date:installation_date,config_status:config_status,comments:comments)
	end
end