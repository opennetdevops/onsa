class AccessPortsController < ApiController
  before_action :set_access_port, only: [:show, :update, :destroy]
  before_action :set_access_node, only: [:create]
  before_action :authenticate_request

  def index
    if params[:location_id]
      @access_nodes = Location.find(params[:location_id]).access_nodes
      all_ports = []

      @access_nodes.each do |an|
        if params[:used]
          all_ports += an.access_ports.where(used:params[:used])
        else
          if params[:multiclient_port]
            all_ports += an.access_ports.where(used:params[:multiclient_port])
          else
            all_ports += an.access_ports
          end
        end
      end
      render json: all_ports
    else
      if params[:multiclient_port]
        @access_ports = []
        @multiclient_access_ports = AccessPort.where(multiclient_port:params[:multiclient_port])
        @multiclient_access_ports.each do |ap|
          an = AccessNode.find(ap.access_node_id)
          my_ap = ap.attributes
          my_ap['access_node'] = an.hostname
          @access_ports << my_ap
        end
      else
        if params[:used]
          @access_ports = AccessPort.where(used:params[:used])
        else
          @access_ports = AccessPort.all
        end
      end
      render json: @access_ports   
    end
  end

  def show
    render json: @access_port
  end

  def create
    @access_port = AccessPort.new(access_port_params)
    if @access_node.access_ports<<@access_port
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

    def set_access_node
      @access_node = AccessNode.find(params[:access_node_id])
    end

    def access_port_params
      params.fetch(:access_port,{}).permit(:port,:used,:multiclient_port)
    end
end
