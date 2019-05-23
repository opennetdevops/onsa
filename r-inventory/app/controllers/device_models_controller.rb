class DeviceModelsController < ApiController
  before_action :set_device_model, only: [:show]
  before_action :authenticate_request

  def show
    render json: @device_model
  end
  
  def index
    @device_model = DeviceModel.all
    render json: @device_model
  end

  private
    def set_device_model
      @device_model = DeviceModel.find(params[:id])
    end
end
