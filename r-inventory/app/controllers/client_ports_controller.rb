class ClientPortsController < ApplicationController
  before_action :set_client_port, only: [:show, :update, :destroy]

  def index
    if params[:used]
      client_node = ClientNode.find(client_port_params[:client_node_id])
      @client_ports = client_node.client_ports.where(used:params[:used])
    else
      @client_ports = ClientNode.find(params[:client_node_id].client_ports
    end
    render json: @client_ports
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
      @client_port = ClientPort.find(params[:id])
    end

    def client_port_params
      params.permit(:interface_name,:client_node_id,:used,:service_id)
    end
end
