class ClientNodesController < ApiController
  before_action :set_client_node, only: [:show, :update, :destroy]

  def index
    @client_nodes = ClientNode.all
    render json: @client_nodes
  end

  def show
    render json: @client_node
  end

  def create
    @client_node = ClientNode.new(client_node_params)

    if @client_node.save
      render json: @client_node, status: :created, location: @client_node
    else
      render json: @client_node.errors, status: :unprocessable_entity
    end
  end

  def update
    if @client_node.update(client_node_params)
      render json: @client_node
    else
      render json: @client_node.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @client_node.destroy
  end

  private
    def set_client_node
      @client_node = ClientNode.find(params[:id])
    end

    def client_node_params
      params.fetch(:client_node,{}).permit(:name,:mgmt_ip,:model,:vendor,:client,:uplink_port,:customer_location,:serial_number)
    end
end
