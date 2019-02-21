class AccessPortsController < ApplicationController
	def index
		@access_nodes = Location.find(params[:location_id]).access_nodes

		all_ports = []

    @access_nodes.each do |an|
    	if params[:used]
    		all_ports << an.access_ports.where(used:params[:used])
    	else
    		all_ports << an.access_ports
    	end
    end

		render json: all_ports
		end
end
