repository:=volodymyrsavchenko/esap-gui
latest_tag:=$(shell docker inspect esap_api | jq -r '.[0].RepoDigests[0]' | md5sum  - | cut -c 1-8)

deploy:
	helm upgrade --install esap-gui . --set image.tag=${latest_tag}
	

tag:
	docker tag esap_gui ${repository}:${latest_tag}
	docker push ${repository}:${latest_tag}
