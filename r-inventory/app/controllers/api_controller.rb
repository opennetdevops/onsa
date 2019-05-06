class ApiController < ActionController::API

  private 
	  def authenticate_request
	    @current_user = AuthorizeApiRequest.call(request.headers).result
	    render json: { error: 'Not Authorized' }, status: 401 unless @current_user
	  end
end