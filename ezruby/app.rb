require 'sinatra'

set :public_folder, File.dirname(__FILE__) + '/upload'
set :bind, '0.0.0.0'
get '/' do
  erb :upload_form
end

post '/upload' do

  file = params[:file]
  filepath =settings.public_folder + '/'+file[:filename]
  File.open(filepath, 'wb') { |f| f.write(file[:tempfile].read) }

  "File '#{filepath}' uploaded successfully!"
end

get '/uploads/:filename' do
  
  
  filename = params[:filename]
  if filename.include?('..')
    "no document traval"
  end
  filecontent=open(filename, "r") 
    
  "you file '#{filecontent.gets}'"
end
