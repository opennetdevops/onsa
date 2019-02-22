class AccessPortsController < ApplicationController
  before_action :set_access_port, only: [:show, :update, :destroy]

  def index
    if params[:location_id]
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
    else
      @access_ports = AccessPort.all
      render json: @access_ports   
    end
  end

  def show
    render json: @access_port
  end

  def create
    @access_port = AccessPort.new(access_port_params)

    if @access_port.save
      render json: @access_port, status: :created, location: @access_port
    else
      render json: @access_port.errors, status: :unprocessable_entity
    end
  end

  def update
    if @access_port.update(access_port_params)
      render json: @access_port
    else
      render json: @access_port.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @access_port.destroy
  end

  private
    def set_access_port
      @access_port = AccessPort.find(params[:id])
    end

    def access_port_params
      params.fetch(:access_port,{}).permit(:port,:used,:access_node_id)
    end
end
