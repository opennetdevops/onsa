ActiveAdmin.register AccessPort do
	controller do
      def permitted_params
        params.permit!
      end
    end

	form do |f|		
		f.inputs do
			f.input :access_node, :as => :select, :collection => AccessNode.all
			f.input :port
			f.input :used
			f.input :multiclient_port
			f.input :has_sfp
		 end
	  	f.actions
	end
end