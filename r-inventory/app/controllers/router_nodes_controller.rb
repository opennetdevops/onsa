class RouterNodesController < ApiController
  before_action :set_router_node, only: [:show, :update, :destroy]

  def index
    if params[:location_id]
    @router_nodes = Location.find(params[:location_id]).router_nodes
  	else
    	@router_nodes = RouterNode.all
    end
    render json: @router_nodes
  end

  def show
    render json: @router_node
  end

  def create
    @router_node = RouterNode.new(router_node_params)

    if @router_node.save
      render json: @router_node, status: :created, location: @router_node
    else
      render json: @router_node.errors, status: :unprocessable_entity
    end
  end

  def update
    if @router_node.update(router_node_params)
      render json: @router_node
    else
      render json: @router_node.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @router_node.destroy
  end

  private
    def set_router_node
      @router_node = RouterNode.find(params[:id])
    end

    def router_node_params
      params.fetch(:router_node,{}).permit(:name,:mgmt_ip,:model,:vendor,:location_id,:private_wan_ip,:loopback)
    end
end
