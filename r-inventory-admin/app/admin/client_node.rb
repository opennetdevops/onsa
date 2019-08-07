ActiveAdmin.register ClientNode do
	controller do
      def permitted_params
        params.permit!
      end
    end

	form do |f|
	f.inputs do
		f.input :serial_number
		f.input :location, label:"Hub"
		f.input :name
		f.input :device_model
  		f.input :mgmt_ip, label:"IP Management", :as => :string
		f.input :client
		f.input :uplink_port, as: :tags
		f.input :customer_location
	end
	  f.actions
	end
end
