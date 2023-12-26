export PDI_HOME=$(pwd)
export FILTER_GTK_WARNINGS=true
export SKIP_WEBKITGTK_CHECK=true
export CHEF_SECRET_KEY=magia
cd chef
pip install -r requirements.txt
flask run --host 0.0.0.0 --port 1882 --reload
