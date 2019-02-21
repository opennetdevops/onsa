require 'test_helper'

class VrfsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @vrf = vrfs(:one)
  end

  test "should get index" do
    get vrfs_url, as: :json
    assert_response :success
  end

  test "should create vrf" do
    assert_difference('Vrf.count') do
      post vrfs_url, params: { vrf: {  } }, as: :json
    end

    assert_response 201
  end

  test "should show vrf" do
    get vrf_url(@vrf), as: :json
    assert_response :success
  end

  test "should update vrf" do
    patch vrf_url(@vrf), params: { vrf: {  } }, as: :json
    assert_response 200
  end

  test "should destroy vrf" do
    assert_difference('Vrf.count', -1) do
      delete vrf_url(@vrf), as: :json
    end

    assert_response 204
  end
end
