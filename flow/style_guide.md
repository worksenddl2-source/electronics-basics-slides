# Google Flow 화풍 가이드 (전 강의 공통)

모든 프롬프트 **앞에** 아래 공통 문구를 붙인다. 첫 강의에서 마음에 드는 결과가 나오면
그 이미지를 Flow의 **참조 이미지(ingredient)** 로 지정해 이후 생성에도 계속 사용한다.

## 공통 문구 (복사해서 사용)
```
Clean modern editorial illustration, soft 3D look with gentle gradients and soft shadows,
friendly and approachable for complete beginners, deep navy (#161A33) background,
accent colors: warm amber (#FFB400) for light and energy, cyan (#2EC4E6) for electrons,
coral red (#F25C54) for positive charge. Simple composition with one clear focal point,
generous empty space, 16:9 landscape.
```

## 공통 금지 (Negative)
```
no text, no letters, no numbers, no labels, no watermark, no logo,
no photorealistic faces, no clutter, no busy background
```

## 규칙
- **그림 안에 글자 금지** → 라벨·수식은 PPTX에서 텍스트로 얹는다 (한글 깨짐 방지).
- 전자는 항상 **빛나는 청록색(cyan) 작은 구슬**, (+)는 **코랄 레드**로 통일 → manim 애니메이션과 색이 맞는다.
- 비율 16:9, 가능한 최고 해상도로 내려받기.
- 저장: `flow/inbox/<프롬프트ID>_v<번호>.png` (예: `01_cover_v1.png`)
  → `python scripts/ingest_flow.py` 실행 시 가장 높은 버전이 `assets/illustrations/01/cover.png` 로 들어간다.
