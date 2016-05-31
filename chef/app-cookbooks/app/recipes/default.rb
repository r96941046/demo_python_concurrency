# Run list for the app

include_recipe 'apt'
include_recipe 'redisio'
include_recipe 'python'

user = node[:app][:user]

# User
user user[:name] do
    home "/home/#{user['name']}"
    shell '/bin/bash'
    supports manage_home: true
    action :create
end

# Redis
service 'redisrqworker' do
    action :start
end

# Python
virtual_env_dir = "/home/#{user['name']}/.virtualenvs/"
virtual_env_path = virtual_env_dir + "#{node['python']['virtualenv']['name']}"

directory virtual_env_dir do
    owner user[:name]
    group 'admin'
    action :create
end

python_virtualenv virtual_env_path do
    interpreter "/usr/bin/python"  # the one installed manually (2.7.7)
    owner user[:name]
    group "admin"
    action :create
end

python_pip "/#{user['name']}/requirements.txt" do
    virtualenv virtual_env_path
    options '-r'
    action :install
end
