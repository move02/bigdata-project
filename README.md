영화 평점기반 커뮤니티 (Mobee)
-----

소프트웨어학과
이동영, 구본철, 장윤정


#### 프로젝트를 하게 된 계기
 빅데이터 시스템 설계 과목 프로젝트

 영화 취향이 같은 사람들끼리 할 수 있는 SNS가 있으면 좋겠다고 해서 만들게 되었다.

#### Stack
- Language : Python, Javascript
- Framework : Django, Vue
- DBMS : Mongodb
- Library
    - scikit-learn : K-means clustering에 사용
    - Djongo : Django에서 공식지원을 하지 않는 Mongodb와의 connect을 위해 사용
    - d3.js : 사용자, 영화 데이터 시각화를 위해 사용

#### Diagrams
- 시스템 흐름도
<img src="img/mobee_flow.png" alt="System Flow" width="450"/>

- Class diagram
<img src="img/mobee_models.png" alt="mobee uml" width="450"/>

#### 주요 기능
- 영화 별 평점 확인
<img src="img/mobee_movie_detail.png" alt="mobee uml" width="450"/>
<br>
- 년도별, 장르 인기순위 확인
<img src="img/mobee_graph.png" alt="mobee uml" width="450"/>

<br>
- 평점을 토대로 사용자 그룹핑(Clustering)인
<img src="img/mobee_club.png" alt="mobee uml" width="450"/>

<br>
- 그룹 별 SNS 형 게시판
<img src="img/mobee_board.png" alt="mobee uml" width="450"/>

<br>
- 그룹 별 영화 평점 데이터 시각화
<img src="img/mobee_graph2.png" alt="mobee uml" width="450"/>

<br>
