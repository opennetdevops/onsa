class LogicalUnitsController < ApiController
  before_action :set_logical_unit, only: [:show, :update, :destroy]
  before_action :authenticate_request

  def index
    if params[:router_node_id]
      if params[:used]
        router_node_lus = RouterNode.find(params[:router_node_id]).logical_units
        if params[:used] == "true"
          @logical_units = LogicalUnit.all.where(id:router_node_lus.pluck(:id))
        end
        if params[:used] == "false"
          @logical_units = LogicalUnit.all.where.not(id:router_node_lus.pluck(:id))
        end
      else
        @logical_units = RouterNode.find(params[:router_node_id]).logical_units
      end
    else
      @logical_units = LogicalUnit.all
    end
    render json: @logical_units
  end

  def create
    if params[:router_node_id]
      router_node = RouterNode.find(params[:router_node_id])
      @logical_unit = LogicalUnit.find(params[:logical_unit_id])
      router_node.logical_units << @logical_unit
      render json: @logical_unit, status: :created, location: @logical_unit
    else
      @logical_unit = LogicalUnit.create(id:logical_unit_params[:logical_unit_id])
      if @logical_unit.save
        render json: @logical_unit, status: :created, location: @logical_unit
      else
        render json: @logical_unit.errors, status: :unprocessable_entity
      end
    end
  end

  def destroy
    if params[:router_node_id]
      router_node = RouterNode.find(params[:router_node_id])
      @logical_unit = LogicalUnit.find(params[:id])
      router_node.logical_units.delete(@logical_unit)
    else
      @logical_unit.destroy
    end
  end

  def show
    render json: @logical_unit
  end

  def update
    if @logical_unit.update(logical_unit_params)
      render json: @logical_unit
    else
      render json: @logical_unit.errors, status: :unprocessable_entity
    end
  end

  def destroy
    @logical_unit.destroy
  end

  private
    def set_logical_unit
      @logical_unit = LogicalUnit.find(params[:id])
    end

    def logical_unit_params
      params.fetch(:logical_unit,{}).permit(:logical_unit_id)
    end
end
