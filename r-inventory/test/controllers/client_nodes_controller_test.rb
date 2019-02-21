require 'test_helper'

class ClientNodesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @client_node = client_nodes(:one)
  end

  test "should get index" do
    get client_nodes_url, as: :json
    assert_response :success
  end

  test "should create client_node" do
    assert_difference('ClientNode.count') do
      post client_nodes_url, params: { client_node: {  } }, as: :json
    end

    assert_response 201
  end

  test "should show client_node" do
    get client_node_url(@client_node), as: :json
    assert_response :success
  end

  test "should update client_node" do
    patch client_node_url(@client_node), params: { client_node: {  } }, as: :json
    assert_response 200
  end

  test "should destroy client_node" do
    assert_difference('ClientNode.count', -1) do
      delete client_node_url(@client_node), as: :json
    end

    assert_response 204
  end
end
