require 'test_helper'

class ClientPortsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @client_port = client_ports(:one)
  end

  test "should get index" do
    get client_ports_url, as: :json
    assert_response :success
  end

  test "should create client_port" do
    assert_difference('ClientPort.count') do
      post client_ports_url, params: { client_port: {  } }, as: :json
    end

    assert_response 201
  end

  test "should show client_port" do
    get client_port_url(@client_port), as: :json
    assert_response :success
  end

  test "should update client_port" do
    patch client_port_url(@client_port), params: { client_port: {  } }, as: :json
    assert_response 200
  end

  test "should destroy client_port" do
    assert_difference('ClientPort.count', -1) do
      delete client_port_url(@client_port), as: :json
    end

    assert_response 204
  end
end
