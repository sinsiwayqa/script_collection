# script_collection
QA's script files

# 스크립트 목록
- findExcept

## findExcept
### 개요
${SOHA_SVC}/${SOHA_SVC}/log 디렉터리의 서버 로그 파일들의 exception 을 출력 한다.
고객사에서 수집한 서버 로그에서 exception 을출력 할 수 있다.

## addProxyService
### 개요
Petra 테스트 자동화 프로그램에서 사용할 9개의 보안대상 및 중계리스너를 생성하여 준다.
파라미터로 __**마스터IP**__, __**마스터PORT**__, __**마스터SOHA_SVC**__ 를 입력하여 준다.
해당 프로그램은 Python 2.7.5에서 개발되었으며, 사용시 MySQL 커넥션을 위한 mysql.connector모듈을 요구하며, 해당 모듈은 아래 명령어를 통해 설치 가능하다.
```
pip install mysql.connector
```




