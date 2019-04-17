ActiveAdmin.register ClientNode do
	form do |f|
	f.inputs do
		f.input :location, label:"Hub"
		f.input :name
		f.input :device_model
  		f.input :mgmt_ip, label:"IP Management", :as => :string
		f.input :client
		f.input :uplink_port
		f.input :customer_location
	end
	  f.actions
	end
end
