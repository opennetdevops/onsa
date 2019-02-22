class ClientPortsController < ApplicationController
  before_action :set_client_port, only: [:show, :update, :destroy]
  before_action :set_client_node

  def index
    if params[:used]
      @client_ports = @client_node.client_ports.where(used:params[:used])
    else
      @client_ports = @client_node.client_ports
    end
  end

  def show
    render json: @client_port
  end

  def create
    @client_port = ClientPort.new(client_port_params)

    if @client_port.save
      render json: @client_port, status: :created, location: @client_port
    else
      render json: @client_port.errors, status: :unprocessable_entity
    end
  end

  def update
    if @client_port.update(client_port_params)
      render json: @client_port
    else
      render json: @client_port.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @client_port.destroy
  end

  private
    def set_client_port
      @client_port = @client_node.client_ports.find(params[:id])
    end

    def set_client_node
      @client_node = ClientNode.find(params[:client_node_id])
    end

    def client_port_params
      params.permit(:interface_name,:client_node_id,:used,:service_id)
    end
end
