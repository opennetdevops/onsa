class ManageAuthorization < ActiveAdmin::AuthorizationAdapter
  attr_reader :admin

  def authorized?(action, subject = nil)
    if action == :update || action == :destroy || action == :create
      admin
    else
      true
    end
  end

  def initialize(resource, user)
    @resource = resource
    @user = user
    ActiveDirectory.connect
    @admin=ActiveDirectory.admins.include?(user.email) 
  end

end