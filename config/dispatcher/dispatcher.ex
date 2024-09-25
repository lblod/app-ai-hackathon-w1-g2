defmodule Dispatcher do
  use Matcher
  define_accept_types [
    html: [ "text/html", "application/xhtml+html" ],
    json: [ "application/json", "application/vnd.api+json" ]
  ]

  @any %{}
  @json %{ accept: %{ json: true } }
  @html %{ accept: %{ html: true } }

  define_layers [ :static, :services, :fall_back, :not_found ]

  # In order to forward the 'themes' resource to the
  # resource service, use the following forward rule:
  #
  # match "/themes/*path", @json do
  #   Proxy.forward conn, path, "http://resource/themes/"
  # end
  #
  # Run `docker-compose restart dispatcher` after updating
  # this file.

  get "/jobs/*path" do
    Proxy.forward conn, path, "http://resource/job/"
  end

  get "/aanduidingsobjects/*path" do
    Proxy.forward conn, path, "http://resource/aanduidingsobject/"
  end

  get "/besluits/*path" do
    Proxy.forward conn, path, "http://resource/besluit/"
  end

  get "/concepts/*path" do
    Proxy.forward conn, path, "http://resource/concepts/"
  end

  get "/concept-schemes/*path" do
    Proxy.forward conn, path, "http://resource/concept-schemes/"
  end

  get "/files/:id/download" do
    Proxy.forward conn, [], "http://file/files/" <> id <> "/download"
  end

  get "/files/*path" do
    forward conn, path, "http://resource/files/"
  end

  match "/pipeline/*path" do
    Proxy.forward conn, path, "http://pipeline/"
  end

  match "/sparql/*path" do
    Proxy.forward conn, path, "http://triplestore:8890/sparql/"
  end

  match "/*path", @html do
    Proxy.forward conn, path, "http://frontend/"
  end

  match "/*_", %{ layer: :not_found } do
    send_resp( conn, 404, "Route not found.  See config/dispatcher.ex" )
  end
end
