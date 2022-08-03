repository:=volodymyrsavchenko/esap-api
latest_tag:=$(shell docker inspect esap_api:latest | jq  '.[0].RootFS.Layers' | md5sum  - | cut -c 1-8)
repositoryGUI:=volodymyrsavchenko/esap-gui
latest_tagGUI:=$(shell docker inspect esap_gui:latest | jq -r '.[0].RootFS.Layers' | md5sum  - | cut -c 1-8)

deploy:
	helm upgrade --install esap -f values-cscs.yaml -f values-cscs-secret.yaml . \
	    --set imageAPI.tag=${latest_tag} \
	    --set imageGUI.tag=${latest_tagGUI} ${extra}
	

tag:
	docker tag esap_api ${repository}:${latest_tag}
	docker push ${repository}:${latest_tag}
	docker tag esap_gui ${repositoryGUI}:${latest_tagGUI}
	docker push ${repositoryGUI}:${latest_tagGUI}


