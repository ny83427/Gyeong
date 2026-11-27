# 경(景)

당나라 경교를 다룬 장편 역사소설 《景》의 한국어판입니다.

- `text/`에 장별 한국어 Markdown 원고를 둡니다.
- `tools/contents.json`에 부·권·장 순서와 목차 제목을 둡니다.
- `docs/`의 정적 사이트는 GitHub Pages의 `main` / `docs`를 게시 원본으로 사용합니다.
- 표지는 [중국어판](https://ny83427.github.io/jing/)에서 가져옵니다.

원고를 추가하거나 수정한 뒤 저장소 루트에서 실행합니다.

```sh
python -m pip install Markdown
python tools/build_site.py
```

원고와 생성된 HTML 파일을 함께 커밋합니다.
