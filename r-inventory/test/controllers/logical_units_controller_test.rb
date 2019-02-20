require 'test_helper'

class LogicalUnitsControllerTest < ActionDispatch::IntegrationTest
  setup do
    @logical_unit = logical_units(:one)
  end

  test "should get index" do
    get logical_units_url, as: :json
    assert_response :success
  end

  test "should create logical_unit" do
    assert_difference('LogicalUnit.count') do
      post logical_units_url, params: { logical_unit: {  } }, as: :json
    end

    assert_response 201
  end

  test "should show logical_unit" do
    get logical_unit_url(@logical_unit), as: :json
    assert_response :success
  end

  test "should update logical_unit" do
    patch logical_unit_url(@logical_unit), params: { logical_unit: {  } }, as: :json
    assert_response 200
  end

  test "should destroy logical_unit" do
    assert_difference('LogicalUnit.count', -1) do
      delete logical_unit_url(@logical_unit), as: :json
    end

    assert_response 204
  end
end
