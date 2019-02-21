class AccessNodesController < ApplicationController
  before_action :set_access_node, only: [:show, :update, :destroy]

  def index
    if params[:location_id]
      @access_nodes = Location.find(params[:location_id]).access_nodes
    else
      @access_nodes = AccessNode.all
    end
    render json: @access_nodes
  end

  def show
    render json: @access_node
  end

  def create
    @access_node = AccessNode.new(access_node_params)

    if @access_node.save
      render json: @access_node, status: :created, location: @access_node
    else
      render json: @access_node.errors, status: :unprocessable_entity
    end
  end

  def update
    if @access_node.update(access_node_params)
      render json: @access_node
    else
      render json: @access_node.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @access_node.destroy
  end

  private
    def set_access_node
      @access_node = AccessNode.find(params[:id])
    end

    def access_node_params
      params.permit(:location_id,:name,:mgmt_ip,:model,:vendor,:uplink_interface,:uplink_ports,:provider_vlan,:logical_unit_id)
    end
end
