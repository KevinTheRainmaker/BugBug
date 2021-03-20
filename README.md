# **BugBugLocal**
## 제1회 오아시스 해커톤 BugBug팀
**개발자: 고강빈 / 기획자: 이재선 / 디자이너: 천선**
<br/><br/>

## **1. 프로젝트 소개**

### **간단 소개**
**제 1회 오아시스 해커톤**에 **GIST EECS 소속 이재선 기획자**와 **전남대 디자인 전공 천선 디자이너**가 함께 작업한 결과물입니다.
**키워드 기반 취업 정보 웹 스크래핑 시스템**을 제작하였으며, 유명한 구인구직 사이트인 **사람인**과 **Indeed**의 서비스를 활용하였습니다.
<br/>

### **기술 스택**
- **파이썬**을 기반으로 기능이 구현되었으며, 서버로는 **Flask**가 이용되었습니다.
- 프론트엔드에는 **html**과 **css**가 이용되었으며, **Bootstrap**을 이용해 개발의 편의성을 향상시켰습니다.
- 디자이너와의 유연한 협업을 위하여 **Zepplin**이라는 프로그램이 사용되었습니다.
- **Excel 파일로의 저장** 및 **사용자 메일로의 파일 전송**을 지원합니다.
- 일부 기능은 Web Page 환경에선 구현하지 못하였으며, 전체 기능은 **ForShowing.py** 에서 실행 가능합니다.
<br/><br/>

---
## **2. 추가 개발 예정**
- 현재로서는 **Python List**를 이용한, 이른바 **Fake DB**가 이용되었지만, 추후 데이터베이스 시스템 추가를 통해 **더욱 빠른 검색기능**을 제공할 것이며, 회원 정보 및 회원 개인별 관심 분야 등을 저장하여 **개인 맞춤형 추천 알고리즘**을 개발하는 것을 목표로 하고 있습니다.
<br/><br/>

---
## **3. 시연 영상 및 소개 페이지**
### https://www.notion.so/BugBug-B5-566195bdb1d7488e98b479a41589b3a8
<br/>

---

## **4. 프로젝트 소개 리플렛**
<img width="600px" src="https://user-images.githubusercontent.com/76294398/111862274-a4a0ca00-8997-11eb-8ae6-4baeeb22f343.png"/>

<br/><br/>

## **5. Error Code List**
>### **smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted.** <br/> 
>### You must have entered the wrong email address or the wrong password. If you don't, release 'Allow low-security apps to access your account'.
<br/>

>### **smtplib.SMTPAuthenticationError: (534, b'5.7.9 Application-specific password required.**<br/>
>### These messages often appear when 2-Step-Verification is enabled. Click the URL of the error message to release the 2nd stage of authentication.
<br/>

>### **PermissionError: [Errno 13] Permission denied**<br/>
>### Wrong file path / Do not specify the file name / Do not specify file format / Didn't use \\ or / as the directory delimiter / Too many files / The file is in use by a program other than the development environment