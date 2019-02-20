class LogicalUnitsController < ApplicationController

  def index
    if params[:used]
      router_node_lus = RouterNode.logical_units
      if params[:used] == "true"
      @logical_units = LogicalUnit.all.where(id:router_node_lus.pluck(:id))
      end
      if params[:used] == "false"
      @logical_units = LogicalUnit.all.where.not(id:router_node_lus.pluck(:id))
      end
    else
      @logical_units = RouterNode.find(params[:router_node_id]).logical_units
    end
    render json: @logical_units
  end

  # POST /logical_units
  def create
    @logical_unit = LogicalUnit.new(logical_unit_params)

    if @logical_unit.save
      render json: @logical_unit, status: :created, location: @logical_unit
    else
      render json: @logical_unit.errors, status: :unprocessable_entity
    end
  end

  # DELETE /logical_units/1
  def destroy
    @logical_unit.destroy
  end

  private
    # Use callbacks to share common setup or constraints between actions.
    def set_logical_unit
      @logical_unit = LogicalUnit.find(params[:id])
    end

    # Only allow a trusted parameter "white list" through.
    def logical_unit_params
      params.fetch(:logical_unit, {})
    end
end
