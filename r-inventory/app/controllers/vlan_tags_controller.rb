class VlanTagsController < ApplicationController
  
  def index
    if params[:access_node_id]
      if params[:used]
        access_node_vlan_tags = AccessNode.vlan_tags
        if params[:used] == "true"
        @vlan_tags = VlanTag.all.where(vlan_tag:access_node_vlan_tags.pluck(:vlan_tag))
        end
        if params[:used] == "false"
        @vlan_tags = VlanTag.all.where.not(vlan_tag:access_node_vlan_tags.pluck(:vlan_tag))
        end
      else
        @vlan_tags = AccessNode.find(params[:access_node_id]).vlan_tags
      end
    else
      @vlan_tags = VlanTag.all
    end
    render json: @vlan_tags
  end

  def create
    if params[:access_node_id]
      access_node = AccessNode.find(params[:access_node_id])
      @vlan_tag = VlanTag.find(params[:vlan_tag_id])
      access_node.vlan_tags << @vlan_tag
    else
      @vlan_tag = VlanTag.new(vlan_tag_params)
    end
    render json: @vlan_tag, status: :created, location: @vlan_tag
  end

  def destroy
    @vlan_tag = VlanTag.find(params[:id])
    if params[:access_node_id]
      access_node = AccessNode.find(params[:access_node_id])
      access_node.vlan_tags.delete(@vlan_tag)
    else
      @vlan_tag.destroy  
    end
  end

  private

    def vlan_tag_params
      params.permit(:access_node_id,:vlan_tag)
    end

end
