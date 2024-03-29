## 볼린저 밴드 전략
 - 볼린저 밴드 전략을 통해 수익률을 측정한다.

### 1. 개요
 - 볼린저 밴드의 범위를 벗어난 경우 매수, 매도를 진행한다. (현재는 현물기준 매수만 진행)
 - 매수 시점은 Bollinger Band의 하단 (df['Lower'])의 가격으로 매수진행.

### 2. 데이터
 - 5분봉 데이터를 사용한다.
 - 약 24시간의 데이터 사용.


case 1
 - Bollinger Band의 하단 전량 매수, 상단 전량 매도
 - 손절 기준 : 1%

 - 매수 시간: 2024-02-09 23:20:00, 매수 가격: 63902144.56 
 - 매도 시간: 2024-02-09 23:25:00, 매도 가격: 63111000.00, 현재 자본: 197326.41원, 수익률: -1.24% 
 - 매수 시간: 2024-02-09 23:30:00, 매수 가격: 63708847.04 
 - 매도 시간: 2024-02-10 01:10:00, 매도 가격: 64235649.14, 현재 자본: 198759.18원, 수익률: 0.83% 
 - ...  
 - 매도 시간: 2024-02-11 03:10:00, 매도 가격: 63984712.85, 현재 자본: 196581.11원, 수익률: 0.03% 
 - **최종 자본: 196581.11, 승: 5, 패: 3 승률: 62.50%, 최종 수익률: -1.71%**

case 2
- Bollinger Band의 하단 전량 매수, 상단과 20기간 이동평균선(MA)의 평균값에 전량 매도
- 손절 기준 : 0.5%

- 매수 시간: 2024-02-09 23:20:00, 매수 가격: 63902144.56 
- 매도 시간: 2024-02-09 23:25:00, 매도 가격: 63582633.84, 현재 자본: 198801.05원, 수익률: -0.50% 
- 매수 시간: 2024-02-09 23:50:00, 매수 가격: 63431601.67 
- 매도 시간: 2024-02-10 00:50:00, 매도 가격: 63956255.91, 현재 자본: 200244.97원, 수익률: 0.83%
- ... 
- 매수 시간: 2024-02-10 19:50:00, 매수 가격: 63348658.48 
- 매도 시간: 2024-02-10 20:30:00, 매도 가격: 63735574.74, 현재 자본: 199494.89원, 수익률: 0.61% 
- **최종 자본: 199494.89, 승: 3, 패: 2 승률: 60.00%, 최종 수익률: -0.25%**
 

case 3
- Bollinger Band의 하단 RSI 지표가 30 미만인 경우 전량 매수, 상단과 RSI 지표가 70 이상인 경우 전량 매도
- 손절 기준 : 1%

 - **결과 정리: 최근 데이터로 승률이 약 70~80%가 나오며, 수익률이 1%에 가깝게 나옴.**
 - **범위를 넓게 잡아 약 두달간의 테스트 데이터 결과로는 승률이 66% 정도가 나오지만**
 - **수익률은 -21%가 나오며 손실을 기록**
 

### 3. 결론
 - k값에 무관하게 승률이 20%를 넘지 못함