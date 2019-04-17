ActiveAdmin.register BackboneNode do
	controller do
      def permitted_params
        params.permit!
      end
    end

	form do |f|		
		f.inputs do
			f.input :location, label: "Hub"
			f.input :hostname
	  		f.input :mgmt_ip, label:"IP Management", :as => :string
		    f.input :loopback, :as => :string
			f.input :device_model, :as => :select, :collection => DeviceModel.all
			f.input :serial_number
			f.input :firmware_version
			f.input :ot
			f.input :installation_date, :as => :datepicker
			f.input :config_status
			f.input :comments
			f.input :contract, :as => :select, :collection => Contract.all
		 end
	  f.actions
	end
end