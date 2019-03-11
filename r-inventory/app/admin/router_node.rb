ActiveAdmin.register RouterNode do
	form do |f|
		f.inputs :except => [:mgmt_ip, :private_wan_ip, :loopback]
		f.inputs do
	    f.input :mgmt_ip, :as => :string
	    f.input :private_wan_ip, :as => :string
	    f.input :loopback, :as => :string
	  end
	  f.actions
	end
end
