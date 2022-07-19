repository:=volodymyrsavchenko/esap-api
latest_tag:=$(shell docker inspect esap_api:latest | jq  '.[0].RootFS.Layers' | md5sum  - | cut -c 1-8)

deploy:
	helm upgrade --install esap-api -f values.yaml -f values-secret.yaml . --set image.tag=${latest_tag} ${extra}
	

tag:
	docker tag esap_api ${repository}:${latest_tag}
	docker push ${repository}:${latest_tag}
