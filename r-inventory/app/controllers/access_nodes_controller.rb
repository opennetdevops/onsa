class AccessNodesController < ApplicationController
  def index
    @access_nodes = Location.find(params[:location_id]).access_nodesl
    render json: @access_nodes
  end

  def create
    @access_node = AccessNode.new(access_node_params)

    if @access_node.save
      render json: @access_node, status: :created, location: @access_node
    else
      render json: @access_node.errors, status: :unprocessable_entity
    end
  end

  private
    # Only allow a trusted parameter "white list" through.
    def access_node_params
      params.permit(:location_id,:name,:mgmt_ip,:model,:vendor,:uplink_interface,:uplink_ports,:provider_vlan,:logical_unit_id)
    end
end
