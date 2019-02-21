require 'test_helper'

class AccessNodesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @access_node = access_nodes(:one)
  end

  test "should get index" do
    get access_nodes_url, as: :json
    assert_response :success
  end

  test "should create access_node" do
    assert_difference('AccessNode.count') do
      post access_nodes_url, params: { access_node: {  } }, as: :json
    end

    assert_response 201
  end

  test "should show access_node" do
    get access_node_url(@access_node), as: :json
    assert_response :success
  end

  test "should update access_node" do
    patch access_node_url(@access_node), params: { access_node: {  } }, as: :json
    assert_response 200
  end

  test "should destroy access_node" do
    assert_difference('AccessNode.count', -1) do
      delete access_node_url(@access_node), as: :json
    end

    assert_response 204
  end
end
