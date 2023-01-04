# petra_inst
설치 스크립트를 이용하여 자동으로 Petra를 설치 합니다. 스크립트 실행 시 입력 항목은 다음과 같습니다. Petra OS 계정으로 실행 합니다.

### Usage

petra_inst [option]

|  항목 | 필수/선택 | 기본값 | 설명 |
| :--- | :--- | :--- | :--- |
| -P,  --prodid       | 필수 | | 제품 ID 마스터 - 0 , 제품 - 1부터 순차적 |
| -svc, --sohasvc     | 필수 | | SOHA_SVC - 인스턴스 고유 ID |
| -pv, --petraversion | 필수 | | Petra Version |
| -dp, --dgnetport    | 선택 | 6600 | DgNet Port |
| -jp, --jdbcport     | 선택 | 6700 | MySQL/JDBC Port |
| -kp, --kredport     | 선택 | 6800 | Kred Port |
| -hp, --helperport   | 선택 | 6900 | Helper Port |
| -pb, --permblks     | 선택 | 10000 | permanent block size |
| -tb, --tempblks     | 선택 | 20000 | temporary block size |
| -h,  --host         | 선택 | | hostname or ip address |
| -mn, --mastername   | 부분 필수 | | Master db name - 마스터가 아닌 제품일 경우 입력 - 마스터 SOHA_SVC |
| -mh, --masterhost   | 부분 필수 | | Master host - 마스터가 아닌 제품일 경우 입력 - 마스터 제품 IP |
| -mp, --masterport   | 부분 필수 | | Master DgNet Port - 마스터가 아닌 제품일 경우 입력 - 마스터 제품 DgNet Port |

### example

```bash
petra_inst -P 0 -svc PETRA -pv 4.1.0.4.48
```
