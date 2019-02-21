require 'test_helper'

class VlanTagsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @vlan_tag = vlan_tags(:one)
  end

  test "should get index" do
    get vlan_tags_url, as: :json
    assert_response :success
  end

  test "should create vlan_tag" do
    assert_difference('VlanTag.count') do
      post vlan_tags_url, params: { vlan_tag: {  } }, as: :json
    end

    assert_response 201
  end

  test "should show vlan_tag" do
    get vlan_tag_url(@vlan_tag), as: :json
    assert_response :success
  end

  test "should update vlan_tag" do
    patch vlan_tag_url(@vlan_tag), params: { vlan_tag: {  } }, as: :json
    assert_response 200
  end

  test "should destroy vlan_tag" do
    assert_difference('VlanTag.count', -1) do
      delete vlan_tag_url(@vlan_tag), as: :json
    end

    assert_response 204
  end
end
