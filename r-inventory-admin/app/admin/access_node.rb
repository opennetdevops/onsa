ActiveAdmin.register AccessNode do
	permit_params :location_id, :hostname, :mgmt_ip, :device_model_id, :serial_number,
	  :firmware_version, :ot, :installation_date, :config_status, :comments,
	  :remote_device_id, :remote_ports, :uplink_ports, :contract_id

	form do |f|
		f.inputs do
			f.input :location
			f.input :hostname
	  		f.input :mgmt_ip, label:"IP Management", :as => :string
			f.input :device_model, :as => :select, :collection => DeviceModel.all
			f.input :serial_number
			f.input :firmware_version
			f.input :ot
			f.input :installation_date, :as => :datepicker
			f.input :config_status, :as => :select, :collection => DeviceModel::STATUSES
			f.input :comments
			f.input :remote_device
			f.input :remote_ports
			f.input :uplink_ports, as: :tags, collection: access_node.device_model.uplink_ports_array
			f.input :contract, :as => :select, :collection => Contract.all
		end
	  f.actions
	end

	index do
	  	selectable_column
	  	column :hostname
	  	column :location, :order => :desc
	  	column(:hub) {|access_node| access_node.location.shortname} 
	  	column :mgmt_ip
	  	column :device_model
	  	column :firmware_version
	  	column :config_status
	  	column :installation_date
	  	actions
  	end

	filter :location
	filter :hostname
	filter :mgmt_ip
	filter :firmware_version, :as => :string
	filter :device_model
	filter :serial_number
	filter :ot
	filter :installation_date
	filter :config_status, as: :select, collection: DeviceModel::STATUSES
	filter :comment
	filter :uplink_ports
	filter :updated_at

end
