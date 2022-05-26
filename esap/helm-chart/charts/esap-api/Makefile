repository:=volodymyrsavchenko/esap-api
latest_tag:=$(shell docker inspect esap_api | jq -r '.[0].RepoDigests[0]' | md5sum  - | cut -c 1-8)

deploy:
	helm upgrade --install esap-api . --set image.tag=${latest_tag}
	

tag:
	docker tag esap_api ${repository}:${latest_tag}
	docker push ${repository}:${latest_tag}
