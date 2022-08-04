image_base:=volodymyrsavchenko/esap-

# this should rather be derived from code version
latest_tag_api:=$(shell docker inspect esap_api:latest | jq  '.[0].RootFS.Layers' | md5sum  - | cut -c 1-8)
latest_tag_gui:=$(shell docker inspect esap_gui:latest | jq  '.[0].RootFS.Layers' | md5sum  - | cut -c 1-8)

image_api:=$(image_base)api:$(latest_tag_api)
image_gui:=$(image_base)gui:$(latest_tag_gui)

package:
	(\
	    	set -x; \
		td=$$(mktemp  -d -u --tmpdir esap-ctaepfl-helm-git-XXXX); \
		git clone git@github.com:cta-epfl/cta-epfl.github.io.git $$td; \
		helm package esap -d $$td ; \
		cd $$td; \
		helm --debug repo index .; \
		git add index.yaml; \
		git add *.tgz; \
		git commit -a -m "new esap version"; \
		tar tvf $$(ls -t *gz | head -1); \
		if echo $${DRY:-yes}  | grep yes; then echo git push; else git push origin main; fi \
	)

increment:
	if echo $${DRY:-yes}  | grep yes; then \
	    	echo '\033[31mdry only!\033[0m' \
		bump2version --verbose --dry-run patch --allow-dirty; \
	else \
		bump2version --verbose patch --allow-dirty; \
	fi 


chart-tags:
	cp -v esap/values.yaml esap/values.yaml.backup
	sed '/imageAPI/ {n;n;n;n; /tag:/ {s/".*"/"'$(latest_tag_api)'"/}}' -i esap/values.yaml
	sed '/imageGUI/ {n;n;n;n; /tag:/ {s/".*"/"'$(latest_tag_gui)'"/}}' -i esap/values.yaml
	diff -U 3  esap/values.yaml* || echo "there is an update!"


deploy:
	helm upgrade --install esap -f values-cscs.yaml -f values-cscs-secret.yaml esap \
	    --set imageAPI.tag=${latest_tag_api} \
	    --set imageGUI.tag=${latest_tag_gui} \
	    ${extra}
	

push:
	docker tag esap_api $(image_api)
	docker push $(image_api)
	docker tag esap_gui  $(image_gui)
	docker push $(image_gui)


