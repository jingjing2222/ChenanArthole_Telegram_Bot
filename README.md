# CheonanArthole_Telegram_Bot

## 소개
이 프로젝트는 Azure Functions를 활용하여 Notion 데이터베이스에서 공연 스케줄 정보를 가져와 Telegram 메시지로 보내는 애플리케이션입니다. 
주로 매니저님, 어셔들이 다음 날의 공연 스케줄을 쉽게 확인할 수 있도록 도와줍니다.

## 기능
- **Notion API 사용**: 특정 Notion 데이터베이스에서 공연 관련 정보를 읽어옵니다.
- **공연 스케줄 파싱**: 가져온 데이터에서 필요한 공연 스케줄 정보를 추출합니다.
- **Telegram을 통한 알림**: 추출한 스케줄 정보를 Telegram 메시지로 전송합니다.

## 사용 방법
### 설정
1. Notion API 토큰과 데이터베이스 ID를 설정합니다.
2. Telegram Bot 토큰과 채팅방 ID를 설정합니다.

### 배포
이 애플리케이션은 Azure Functions를 통해 실행됩니다. 
Azure Functions에 대한 자세한 실행 방법은 [Azure 공식 문서](https://docs.microsoft.com/en-us/azure/azure-functions/)를 참고하세요.

### 실행
- 애플리케이션은 매일 아침 8시에 실행되도록 예약되어 있습니다.
- Azure Functions의 `TimerTrigger` 기능을 사용하여 스케줄링합니다.

## 개발 환경
- Python 3.x
- Azure Functions
- Notion API
- Telegram Bot API
