require 'test_helper'

class RouterNodesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @router_node = router_nodes(:one)
  end

  test "should get index" do
    get router_nodes_url, as: :json
    assert_response :success
  end

  test "should create router_node" do
    assert_difference('RouterNode.count') do
      post router_nodes_url, params: { router_node: {  } }, as: :json
    end

    assert_response 201
  end

  test "should show router_node" do
    get router_node_url(@router_node), as: :json
    assert_response :success
  end

  test "should update router_node" do
    patch router_node_url(@router_node), params: { router_node: {  } }, as: :json
    assert_response 200
  end

  test "should destroy router_node" do
    assert_difference('RouterNode.count', -1) do
      delete router_node_url(@router_node), as: :json
    end

    assert_response 204
  end
end
