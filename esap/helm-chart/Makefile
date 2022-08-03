latest_api_tag:=$(shell docker inspect esap_api:latest | jq  '.[0].RootFS.Layers' | md5sum  - | cut -c 1-8)
latest_gui_tag:=$(shell docker inspect esap_gui:latest | jq  '.[0].RootFS.Layers' | md5sum  - | cut -c 1-8)

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
	bump2version --verbose --dry-run patch --allow-dirty


chart-tags:
	cp -v esap/values.yaml esap/values.yaml.backup
	sed '/imageAPI/ {n;n;n;n; /tag:/ {s/".*"/"'$(latest_api_tag)'"/}}' -i esap/values.yaml
	sed '/imageGUI/ {n;n;n;n; /tag:/ {s/".*"/"'$(latest_gui_tag)'"/}}' -i esap/values.yaml
	diff -U 3  esap/values.yaml*
