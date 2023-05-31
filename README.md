# DVS 부하 및 성능 테스트 용 locust script

##env
python 3.9 사용
[pakage관리]
poetry
```
#최초 패키지 dependency 설정 
poerty install
```

###Run
```
# i 옵션은 테스트할 유저수를 고정하고 싶을때 사용. 옵션이므로 생략해도 무방
#단일 실행
locust -f locustfiles -i [테스트할 유저 수]

#User Class 선택 가능 실행
locust -f locustfiles --class-picker -i [테스트할 유저 수]

```

###Docker 실행
```
#docker compose 파일 추가 할 예정
#image build
docker build -t locust .

#worker 실행. 
docker run --name locust_worker -p 8089:8089 --mount type=bind,src=$PWD/reports,dst=/code/reports locust -f locustfiles --class-picker --worker --master-host=[master ip]

```