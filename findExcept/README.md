# script_collection
QA's script files

## findExcept
### 개요
${SOHA_SVC}/${SOHA_SVC}/log 디렉터리의 서버 로그 파일들의 exception 을 출력 한다.
고객사에서 수집한 서버 로그에서 exception 을출력 할 수 있다.

### 사용법
```console
>$ ./findExcept <file|directory>
```

### 동작 방식
1. SOHA_HOME, SOHA_SVC 환경 변수가 설정 되어 있는 경우, ${SOHA_HOME}/${SOHA_SVC}/log 디렉터리의 모든 서버 로그 파일에서 exception 을 출력 한다.
2. 인자 값으로 특정 파일명을 입력 시, 입력한 파일에서 exception 을 출력 한다.
3. 인자 값으로 특정 디렉터리를 입력 시, 입력한 디렉터리 내의 서버 로그파일에서 exception 을 출력 한다.

### 필수 파일
- findExcept shell script file
- findExcept.awk awk file
- .exception text file
- common.sh shell script file




