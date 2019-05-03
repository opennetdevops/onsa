module ActiveDirectory

  DOMAIN_CONTROLLER = "int.fibercorp.com.ar"
  LDAP_PORT = "389"
  BASE = "DC=int,DC=fibercorp,DC=com,DC=ar"	
  USERNAME = "app_apiw"
  PASSWORD = "fcQmuSQngeZo6CywpR6v"
  ADMIN_GROUP = "CN=Grupo App_FIPAM_Operator,OU=OU Grupos,OU=OU Hornos,DC=int,DC=fibercorp,DC=com,DC=ar"

  def self.connect
    @ldap = Net::LDAP.new  :host => DOMAIN_CONTROLLER, # your LDAP host name or IP goes here,
		                          :port => LDAP_PORT, # your LDAP host port goes here,
		                          :base => BASE, # the base of your AD tree goes here,
		                          :auth => {
		                        :method => :simple,
		                        :username => USERNAME, # a user w/sufficient privileges to read from AD goes here,
		                        :password => PASSWORD # the user's password goes here
    }
  end

  def self.connection_ok?
	 @ldap.bind
  end

  def self.query_by_user(userPrincipalName)
    treebase = ActiveDirectory::BASE
    attributes = ["dn", "givenName", "memberOf", "userPrincipalName", "member"]
  	filter = Net::LDAP::Filter.eq("userPrincipalName", userPrincipalName)
	  result = @ldap.search(:base => treebase, :filter => filter, :attributes => attributes) { |item|  
	   return item  		
    }  
  end

  def self.admins
    treebase = ActiveDirectory::BASE
    attributes = ["userPrincipalName"]
    #Define admin user group
    filter = "(&(objectClass=user)(memberOf:1.2.840.113556.1.4.1941:=#{ActiveDirectory::ADMIN_GROUP}))"
    admins = []
    @ldap.search(:base => treebase, :filter => filter, :attributes => attributes) do |entry|
      admins << entry[:userPrincipalName][0]
    end
    return admins
  end

end