package:
	(\
		td=$$(mktemp  -d -u --tmpdir esap-ctaepfl-helm-git-XXXX); \
		git clone git@github.com:cta-epfl/cta-epfl.github.io.git $$td; \
		helm package esap -d $$td ; \
		cd $$td; helm repo index .; \
		git add *.tgz; \
		git commit -a -m "new esap version"; \
		tar tvf $$(ls -t *gz | head -1); \
		echo git push; \
	)

increment:
	bump2version --verbose --dry-run --current-version 0.1.2 patch --allow-dirty
