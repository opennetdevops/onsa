require 'test_helper'

class AccessPortsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @access_port = access_ports(:one)
  end

  test "should get index" do
    get access_ports_url, as: :json
    assert_response :success
  end

  test "should create access_port" do
    assert_difference('AccessPort.count') do
      post access_ports_url, params: { access_port: {  } }, as: :json
    end

    assert_response 201
  end

  test "should show access_port" do
    get access_port_url(@access_port), as: :json
    assert_response :success
  end

  test "should update access_port" do
    patch access_port_url(@access_port), params: { access_port: {  } }, as: :json
    assert_response 200
  end

  test "should destroy access_port" do
    assert_difference('AccessPort.count', -1) do
      delete access_port_url(@access_port), as: :json
    end

    assert_response 204
  end
end
