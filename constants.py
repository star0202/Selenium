VERSION = "1.0.0"
DAYS = ["월", "화", "수", "목", "금", "토", "일"]
COVID_SELECTORS = {
    "death": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_graph > table > tbody > tr:nth-child(1) > td:nth-child(2) > span",
    "confirmed": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_graph > table > tbody > tr:nth-child(1) > td:nth-child(5) > span",
    "total_death": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_num > div:nth-child(1)",
    "total_confirmed": "#content > div > div > div > div.liveToggleOuter > div > div.live_left > div.occurrenceStatus > div.occur_num > div:nth-child(2)"
}
HELP_SELECT_RAW = {
    "/급식": "급식을 출력합니다.",
    "/도움말": "도움말을 출력합니다.",
    "/등록": "학생 데이터를 등록합니다.",
    "/등록해제": "학생 데이터를 등록 해제합니다.",
    "/봇": "봇의 정보를 출력합니다.",
    "/서버정보": "서버의 정보를 출력합니다.",
    "/소스코드": "봇의 소스코드 링크를 출력합니다.",
    "/시간표": "시간표를 출력합니다.",
    "/유저정보": "유저의 정보를 출력합니다.",
    "/코로나": "코로나 현황을 출력합니다.",
    "/핑": "봇의 핑을 출력합니다."
}
HELP_EMBED_RAW = {
    "/급식": "그날의 급식을 출력합니다. 아래에 있는 버튼으로 날짜 조정, 영양소 표시를 할 수 있습니다.",
    "/도움말": "도움말을 출력합니다.",
    "/등록 `[학년]` `[반]`": "학생 데이터를 `[학년]` `[반]`으로 저장합니다.",
    "/등록해제": "학생 데이터를 삭제합니다.",
    "/봇": "봇의 정보를 출력합니다.",
    "/서버정보": "서버의 정보를 출력합니다.",
    "/소스코드": "봇 깃허브 레포지토리 링크를 출력합니다.",
    "/시간표 `(학년)` `(반)`": "`(학년)` `(반)`의 그 주 시간표를 출력합니다. /등록 명령어로 학생 데이터를 등록하면 학년과 반을 입력할 필요가 없습니다.",
    "/유저정보 `(유저)`": "`(유저)`의 정보를 출력합니다. `(유저)`를 입력하지 않으면 자신의 정보를 출력합니다.",
    "/코로나": "코로나 현황을 출력합니다.",
    "/핑": "봇의 핑을 출력합니다."
}
