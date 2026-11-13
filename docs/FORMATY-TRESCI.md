# Format danych: JSON-HTML i JSON-IMAGE

Wszystkie pliki edytujesz w Notepad++ lub VS Code jako UTF-8. JSON **nie pozwala na komentarze**, a ostatni element tablicy/obiektu nie może mieć przecinka.

## 1. `public/content/site.json`

Lista zakładek. Przykład wpisu:

```json
{"id":"diagramy", "label":"DevOps - grafiki", "file":"content/diagramy/page.json"}
```

`id` musi być unikalnym identyfikatorem z małych liter, cyfr, myślników i podkreślników. `file` wskazuje `page.json` względem `public/`.

## 2. `page.json` — wybór sposobu prezentacji

### JSON-HTML

```json
{
  "id":"lokalnie",
  "type":"json-html",
  "title":"DevOps - lokalnie",
  "heading":"WSL2 + Docker + DDEV",
  "subtitle":"Polecenia i ich opisy",
  "notice":"",
  "sections":["sections/sekcja-01.json"]
}
```

### JSON-IMAGE

```json
{
  "id":"diagramy",
  "type":"json-image",
  "title":"DevOps - grafiki",
  "heading":"Schematy",
  "subtitle":"Instrukcje obrazkowe",
  "notice":"",
  "sections":["sections/sekcja-01.json"]
}
```

Brak `type` jest traktowany jako `json-html` (zgodność z wersją 1); w wersji 2 wpisuj typ jawnie.

## 3. Plik sekcji JSON-HTML

```json
{
  "id":"sekcja-01",
  "title":"01 · Podstawy",
  "summary":"Wprowadzenie",
  "subsections":[
    {
      "id":"terminal",
      "title":"Terminal",
      "commands":[
        {"command":"git status", "description":"Pokazuje bieżące zmiany."}
      ]
    }
  ]
}
```

Widok: wszystkie sekcje są umieszczone na stronie jedna pod drugą; spis treści przewija do odpowiedniej sekcji lub podsekcji. Każda komenda posiada przycisk kopiowania.

## 4. Plik sekcji JSON-IMAGE

```json
{
  "id":"sekcja-01",
  "title":"01 · Grafiki lokalne",
  "summary":"Wybierz diagram w menu.",
  "images":[
    {
      "id":"schemat-1",
      "title":"Schemat systemu",
      "src":"content/diagramy/sections/images/schemat-1.jpg",
      "alt":"Opis zawartości diagramu",
      "description":"Tekst nad obrazkiem",
      "caption":"Tekst pod obrazkiem"
    },
    {
      "id":"schemat-2",
      "title":"Drugi schemat",
      "src":"content/diagramy/sections/images/schemat-2.png",
      "alt":"Opis drugiego diagramu"
    }
  ]
}
```

**Wymagane** w obrazie: `id`, `title`, `src`, `alt`. **Opcjonalne**: `description`, `caption`. Plik musi istnieć fizycznie w `public/content/NAZWA_ZAKLADKI/sections/images/` i mieć rozszerzenie `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif` lub `.svg`.

Widok: menu boczne pokazuje pogrupowane tytuły grafik; kliknięcie w grafikę zmienia pojedynczy widok w prawej części. Aktywny obraz ma własny adres `#/ID_STRONY/ID_SEKCJI/ID_OBRAZU`.

## 5. Organizacja obrazów w katalogach zakładek

Każda zakładka typu `json-image` przechowuje **swoje** grafiki w katalogu `public/content/NAZWA_ZAKLADKI/sections/images/` (wspólnym dla sekcji wewnątrz tej zakładki). Przykładowo:

```text
public/content/
├── diagramy/
│   ├── page.json
│   └── sections/
│       ├── sekcja-01.json
│       ├── sekcja-02.json
│       └── images/
│           ├── architektura.jpg
│           └── github-actions.jpg
└── instrukcje/
    ├── page.json
    └── sections/
        ├── sekcja-01.json
        └── images/
            └── krok-1.png
```

W polu `src` wpisz **pełną ścieżkę względem katalogu `public/`**, np. `content/diagramy/sections/images/architektura.jpg`. Nie wpisuj wyłącznie `images/architektura.jpg`. Walidator odrzuci obrazy odwołujące się do katalogu innej zakładki.

## 6. Wskazówki

- Dla własnych obrazów stosuj krótkie, stabilne nazwy, np. `deploy-01.jpg`.
- Unikaj bardzo ciężkich plików — dla zdjęć zwykle wystarcza JPEG lub WebP; dla zrzutów ekranu PNG lub WebP.
- Nie wpisuj ścieżek rozpoczynających się od `/`, aby GitHub Pages działał w podkatalogu repozytorium.
- `alt` powinien opisywać informację przedstawioną na ilustracji, nie tylko mówić „obrazek”.
- Po dodaniu pliku uruchom `python3 scripts/validate.py`.
- Obrazy publikowane na GitHub Pages stają się publicznie dostępne.
