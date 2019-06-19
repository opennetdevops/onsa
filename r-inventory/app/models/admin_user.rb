class AdminUser < ApplicationRecord
  # Include default devise modules. Others available are:
  # :confirmable, :lockable, :timeoutable and :omniauthable
  devise :ldap_authenticatable

  def login_with
    puts self.class.name.to_s
    b = Devise.mappings[:self.class.name.to_s]
    puts Devise.mappings
    puts "a"
    a = Devise.mappings.find {|k,v| v.class_name == self.class.name}
    puts a
    @login_with ||= Devise.mappings.find {|k,v| v.class_name == self.class.name}.last.to.authentication_keys.first
    self[@login_with]
  end
end
