package:
	git clone git@github.com:cta-epfl/cta-epfl.github.io.git /tmp/cta-epfl.github.io ||\
	(cd /tmp/cta-epfl.github.io; git checkout main; git pull)
	helm package esap -d /tmp/cta-epfl.github.io
	(cd /tmp/cta-epfl.github.io; helm repo index .; git add *; git commit -a -m "new esap version"; git push)

increment:
	bump2version --verbose --dry-run --current-version 0.1.2 patch --allow-dirty
