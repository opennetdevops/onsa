class VlansController < ApplicationController
  
  def index
    if params[:access_node_id]
      if params[:used]
        access_node_vlan_tags = AccessNode.vlans
        if params[:used] == "true"
        @vlans = Vlan.all.where(vlan_tag:access_node_vlans.pluck(:vlan_tag))
        end
        if params[:used] == "false"
        @vlans = Vlan.all.where.not(vlan_tag:access_node_vlans.pluck(:vlan_tag))
        end
      else
        @vlans = AccessNode.find(params[:access_node_id]).vlans
      end
    else
      @vlans = Vlan.all
    end
    render json: @vlans
  end

  def create
    if params[:access_node_id]
      access_node = AccessNode.find(params[:access_node_id])
      @vlan = Vlan.find(params[:vlan_tag_id])
      access_node.vlans << @vlan
    else
      @vlan = Vlan.new(vlan_params)
    end
    render json: @vlan, status: :created, location: @vlan
  end

  def destroy
    @vlan = Vlan.find(params[:id])
    if params[:access_node_id]
      access_node = AccessNode.find(params[:access_node_id])
      access_node.vlans.delete(@vlan)
    else
      @vlan.destroy  
    end
  end

  private

    def vlan_params
      params.fetch(:vlan,{}).permit(:access_node_id,:vlan_tag)
    end

end
