.FORCE:
up: .FORCE
	docker-compose -f cta/docker-compose.yml up --build -d

down:
	docker-compose -f cta/docker-compose.yml down

push: .FORCE
	docker-compose -f cta/docker-compose.yml push
