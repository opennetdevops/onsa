ActiveAdmin.register RouterNode do
	controller do
      def permitted_params
        params.permit!
      end
    end

	form do |f|		
		f.inputs do
			f.input :location
			f.input :hostname
	  	f.input :mgmt_ip, label:"IP Management", :as => :string
		  f.input :private_wan_ip, label:"Private WAN IP (Virtual CPE)", :as => :string
		  f.input :loopback, :as => :string
			f.input :device_model, :as => :select, :collection => DeviceModel.all
			f.input :serial_number
			f.input :firmware_version
			f.input :ot
			f.input :installation_date, :as => :datepicker
			f.input :config_status, :as => :select, :collection => DeviceModel::STATUSES
			f.input :comments
			f.input :contract, :as => :select, :collection => Contract.all
		end
	  f.actions
	end

	index do
    	selectable_column
    	column :hostname
    	column :location, :order => :desc
    	column(:hub) {|router_node| router_node.location.shortname} 
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
