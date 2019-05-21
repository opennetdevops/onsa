ActiveAdmin.register DeviceModel do
	permit_params :brand, :model, :end_of_life, :end_of_support, :uplink_ports

	form do |f|
		f.inputs do
			f.input :brand
			f.input :model
	  		f.input :end_of_life, :as => :datepicker
	  		f.input :end_of_support, :as => :datepicker
			f.input :uplink_ports, as: :tags
		end
	  f.actions
	end

end