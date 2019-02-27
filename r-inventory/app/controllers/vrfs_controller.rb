class VrfsController < ApiController
  before_action :set_vrf, only: [:show, :update, :destroy]

  def index
    if params[:location_id]
      @vrfs = Location.find(:location_id).vrfs
    else
      if params[:client]
        @vrfs = Vrf.where(client:params[:client])
      elsif params[:used]
        @vrfs = Vrf.where.(used:params[:used])
      else
        @vrfs = Vrf.all
      end
    end
    render json: @vrfs
  end

  def show
    if params[:location_id]
      @vrfs = Location.find(:location_id).vrfs.find(params[:id])
    else
      render json: @vrf
    end
  end

  def create
    if params[:location_id]
      location = Location.find(params[:location_id])
      @vrf = Vrf.find(params[:vrf_id])
      location.vrfs << @vrf
      render json: @vrf, status: :created, location: @vrf
    else
      @vrf = Vrf.create(vrf_params)
      if @vrf.save
        render json: @vrf, status: :created, location: @vrf
      else
        render json: @vrf.errors, status: :unprocessable_entity
      end
    end
  end

  def update
    if @vrf.update(vrf_params)
      render json: @vrf
    else
      render json: @vrf.errors, status: :unprocessable_entity
    end
  end

  def destroy
    if params[:location_id]
      location = Location.find(params[:location_id])
      location.vrfs.delete(@vrf)
    else
      @vrf.destroy
    end
  end

  private
    def set_vrf
      @vrf = Vrf.find(params[:id])
    end

    def vrf_params
      params.fetch(:vrf,{}).permit(:rt,:name,:used,:description,:client)
    end
end
