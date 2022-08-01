repository:=volodymyrsavchenko/esap-api
latest_tag:=$(shell docker inspect esap_api:latest | jq  '.[0].RootFS.Layers' | md5sum  - | cut -c 1-8)

deploy:
	helm upgrade --install esap-api -f values.yaml -f values-secret.yaml . --set image.tag=${latest_tag} ${extra}
	

tag:
	docker tag esap_api ${repository}:${latest_tag}
	docker push ${repository}:${latest_tag}


repositoryGUI:=volodymyrsavchenko/esap-gui
latest_tagGUI:=$(shell docker inspect esap_gui:latest | jq -r '.[0].RepoDigests[0]' | md5sum  - | cut -c 1-8)

deployGUI:
	helm upgrade --install esap-gui . --set image.tag=${latest_tagGUI} ${extraGUI}
	

tagGUI:
	docker tag esap_gui ${repositoryGUI}:${latest_tagGUI}
	docker push ${repositoryGUI}:${latest_tagGUI}
