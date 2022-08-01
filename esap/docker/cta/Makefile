.FORCE:
up: .FORCE
	docker-compose -f docker-compose.yml up --build -d

down:
	docker-compose -f docker-compose.yml down

push: .FORCE
	docker-compose -f docker-compose.yml push
