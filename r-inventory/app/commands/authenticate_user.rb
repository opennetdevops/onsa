class AuthenticateUser
  prepend SimpleCommand

  def initialize(email, password)
    @email = email
    @password = password
  end

  def call
    JsonWebToken.encode(user_id: user.id) if user
  end

  private

  attr_accessor :email, :password

  def user
    user = AdminUser.find_by_email(email)

    if user.nil?
      user = AdminUser.new(email:email)
      if user.valid_ldap_authentication?(password)
        user.save
        return user
      end
    end

    return user if user.valid_ldap_authentication?(password)

    errors.add :user_authentication, 'invalid credentials'
    nil
  end
end