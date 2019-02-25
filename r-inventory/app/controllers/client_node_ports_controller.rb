class ClientNodePortsController < ApplicationController
  before_action :set_client_node_port, only: [:show, :update, :destroy]
  before_action :set_client_node, only: [:create, :show, :index]

  def index
    if params[:used]
      @client_node_ports = @client_node.client_node_ports.where(used:params[:used])
    else
      @client_node_ports = @client_node.client_node_ports
    end
    render json: @client_node_ports
  end

  def show
    render json: @client_node_port
  end

  def create
    @client_node_port = ClientNodePort.new(client_node_port_params)
    if @client_node.client_node_ports<<@client_node_port
      render json: @client_node_port, status: :created, location: [@client_node,@client_node_port]
    else
      render json: @client_node_port.errors, status: :unprocessable_entity
    end
  end

  def update
    if @client_node_port.update(client_node_port_params)
      render json: @client_node_port
    else
      render json: @client_node_port.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @client_node_port.destroy
  end

  private
    def set_client_node_port
      @client_node_port = @client_node.client_node_ports.find(params[:id])
    end

    def set_client_node
      @client_node = ClientNode.find(params[:client_node_id])
    end

    def client_node_port_params
      params.fetch(:client_node_port,{}).permit(:interface_name,:used,:service_id)
    end
end
