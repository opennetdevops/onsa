class DeviceModelsController < ApplicationController

  def uplink_ports
  	render json: DeviceModel.find(params[:id]).uplink_ports_array
  end

end