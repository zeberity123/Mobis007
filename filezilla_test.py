# [1] 모듈 임포트
import ftplib

# [2] 서버 접속
ftp = ftplib.FTP(host='192.168.100.60')

# [3] 사용자 로그인
res = ftp.login(user='Curation_data', passwd='Curation_data')
print(res)

# [4] 연결 닫기
res = ftp.quit()
print(res)
