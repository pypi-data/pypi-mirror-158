.PHONY: upgrade-pollination-react

.PHONY: generate-frontend

.PHONY: dev-install-package

upgrade-pollination-react:
	yarn --cwd pollination_streamlit_io/auth_user/frontend add pollination-react-io@latest
	yarn --cwd pollination_streamlit_io/get_geometry/frontend add pollination-react-io@latest
	yarn --cwd pollination_streamlit_io/get_hbjson/frontend add pollination-react-io@latest
	yarn --cwd pollination_streamlit_io/get_host/frontend add pollination-react-io@latest
	yarn --cwd pollination_streamlit_io/send_geometry/frontend add pollination-react-io@latest
	yarn --cwd pollination_streamlit_io/send_hbjson/frontend add pollination-react-io@latest
	yarn --cwd pollination_streamlit_io/send_results/frontend add pollination-react-io@latest

add-deps:
	yarn --cwd pollination_streamlit_io/get_geometry/frontend add  url stream-browserify https-browserify assert tty-browserify os-browserify browserify-zlib fs-browser path-browserify path-browserify stream-http util buffer
	yarn --cwd pollination_streamlit_io/get_hbjson/frontend add    url stream-browserify https-browserify assert tty-browserify os-browserify browserify-zlib fs-browser path-browserify path-browserify stream-http util
	yarn --cwd pollination_streamlit_io/get_host/frontend add      url stream-browserify https-browserify assert tty-browserify os-browserify browserify-zlib fs-browser path-browserify path-browserify stream-http util
	yarn --cwd pollination_streamlit_io/send_geometry/frontend add url stream-browserify https-browserify assert tty-browserify os-browserify browserify-zlib fs-browser path-browserify path-browserify stream-http util
	yarn --cwd pollination_streamlit_io/send_hbjson/frontend add   url stream-browserify https-browserify assert tty-browserify os-browserify browserify-zlib fs-browser path-browserify path-browserify stream-http util
	yarn --cwd pollination_streamlit_io/send_results/frontend add  url stream-browserify https-browserify assert tty-browserify os-browserify browserify-zlib fs-browser path-browserify path-browserify stream-http util

generate-frontend:
	yarn --cwd pollination_streamlit_io/auth_user/frontend build
	yarn --cwd pollination_streamlit_io/get_geometry/frontend build
	yarn --cwd pollination_streamlit_io/get_hbjson/frontend build
	yarn --cwd pollination_streamlit_io/get_host/frontend build
	yarn --cwd pollination_streamlit_io/send_geometry/frontend build
	yarn --cwd pollination_streamlit_io/send_hbjson/frontend build
	yarn --cwd pollination_streamlit_io/send_results/frontend build
