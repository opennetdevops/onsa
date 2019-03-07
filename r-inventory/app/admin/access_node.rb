ActiveAdmin.register AccessNode do
	form do |f|
		f.inputs :except => [:mgmt_ip] 
		f.inputs do
	  	f.input :mgmt_ip, :as => :string
		end
	  f.actions
	end
end
