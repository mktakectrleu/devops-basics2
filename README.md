# DevOps Basics 2

Modularna dokumentacja WWW oparta na **HTML + CSS + JavaScript + JSON**. Działa lokalnie w **WSL2 / Ubuntu + Docker + DDEV** oraz na **GitHub Pages**. **Nie wymaga Node.js, bazy danych ani frameworka JS**.

## Co nowego w wersji 2?

Aplikacja obsługuje **dwa sposoby prezentacji treści strony**:

| Tryb | Przeznaczenie | Zachowanie menu bocznego |
| --- | --- | --- |
| `json-html` | Dotychczasowe sekcje, podsekcje, komendy i opisy | Kliknięcie przenosi do sekcji w długiej stronie. |
| `json-image` | Dokumentacja ilustrowana plikami JPG, JPEG, PNG, WebP, GIF lub SVG | Kliknięcie pozycji wybiera **jedną** grafikę widoczną po prawej. |

Zachowano 3 stare zakładki (`DevOps - lokalnie`, `DevOps - GitHub`, `DevOps - VS Code`) wraz z **186 komendami**. Dodano 4. zakładkę `DevOps - grafiki` z 3 sekcjami i 4 przykładowymi grafikami JPEG (możesz je wymienić na swoje). Łącznie 22 sekcje.

`topbar` i `hero` pozostają przyklejone u góry. Menu boczne zachowuje mechanizm inteligentnego odsłaniania aktywnej pozycji bez widocznego scrollbara. Na telefonach menu jest rozwijane. W obu trybach działa wyszukiwanie, a w `json-html` również kopiowanie komend. W `json-image` dostępne są przyciski poprzednia/następna, strzałki klawiatury i otwieranie oryginału.

## Struktura projektu

```text
devops-basics-2/
├── .ddev/config.yaml                  # projekt DDEV, docroot public
├── .github/workflows/
│   ├── ci.yml                         # testy w Pull Request i gałęziach
│   └── pages.yml                      # automatyczny build/deploy main
├── .vscode/                           # wspólna konfiguracja edytora
├── public/
│   ├── index.html                     # szablon strony
│   ├── styles.css                     # wygląd, także sticky topbar/hero
│   ├── app.js                         # renderer dwóch trybów
│   ├── .nojekyll
│   ├── assets/images/                # lokalne pliki graficzne
│   └── content/
│       ├── site.json                  # lista zakładek głównych
│       ├── lokalnie/                  # json-html
│       ├── github/                    # json-html
│       ├── vscode/                    # json-html
│       └── diagramy/                  # json-image
│           ├── page.json
│           └── sections/
│               ├── sekcja-01.json
│               ├── sekcja-02.json
│               └── sekcja-03.json
├── scripts/
│   ├── validate.py                    # sprawdza JSON i pliki obrazów
│   └── build.py                       # kopiuje public/ do dist/
├── tests/test_project.py
├── docs/FORMATY-TRESCI.md             # instrukcja edycji obu formatów
└── README.md
```

## Uruchomienie lokalne w DDEV

Rozpakuj ZIP w Ubuntu (WSL2), zachowując nazwę katalogu `devops-basics-2`:

```bash
cd ~/projekty/devops-basics-2
ddev start
ddev launch
```

Adres: **https://devops-basics-2.ddev.site**. Zapisz zmiany w plikach `public/` i odśwież stronę; **nie musisz robić commita ani restartować DDEV**.

Alternatywa bez DDEV (z katalogu projektu):

```bash
python3 -m http.server 8000 --directory public
```

Adres: http://localhost:8000. Nie uruchamiaj przez `file://`, bo aplikacja używa `fetch()` do odczytu JSON.

## Jak dodać nową grafikę (JSON-IMAGE)?

1. Wstaw np. `moja-instrukcja.jpg` do `public/assets/images/`.
2. Edytuj `public/content/diagramy/sections/sekcja-01.json` w Notepad++ lub VS Code.
3. Dopisz obiekt do listy `images`:

```json
{
  "id": "moja-instrukcja",
  "title": "Moja instrukcja",
  "src": "assets/images/moja-instrukcja.jpg",
  "alt": "Opis obrazka dla osób niewidomych",
  "description": "Krótki opis widoczny nad grafiką",
  "caption": "Opcjonalny podpis pod ilustracją"
}
```

Nie trzeba zmieniać `app.js` ani `index.html`. Każda dodana grafika staje się nową pozycją menu bocznego; po kliknięciu pokazywany jest **tylko wybrany obraz**. Wartość `src` jest ścieżką od katalogu `public/`, bez ukośnika na początku (np. `assets/images/plik.jpg`). Unikaj spacji i polskich liter w nazwach samych plików. Pliki obrazów mogą być dowolnej orientacji — dopasowanie rozmiaru realizuje CSS.

Aby dodać **nową sekcję obrazów**, utwórz plik `sections/sekcja-04.json` na wzór istniejących i dopisz `"sections/sekcja-04.json"` do tablicy `sections` w `content/diagramy/page.json`.

Aby dodać **nową zakładkę** trybu `json-image`, utwórz jej `page.json` oraz `sections/*.json`, a następnie dodaj wpis w `public/content/site.json`.

Pełne schematy i przykłady: [docs/FORMATY-TRESCI.md](docs/FORMATY-TRESCI.md).

## Adresy prowadzące do konkretnej grafiki

Przykład:

```text
https://devops-basics-2.ddev.site/#/diagramy/sekcja-01/architektura
```

W GitHub Pages adres analogicznie zawiera prefiks repozytorium. Kliknięcie pozycji menu zmienia hash URL, więc można zapamiętać link do konkretnego obrazu.

## Walidacja, testy i budowanie

```bash
cd ~/projekty/devops-basics-2
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

Walidator sprawdza unikalność ID, wymaganą treść, bezpieczeństwo ścieżek i istnienie plików graficznych. `build.py` tworzy katalog `dist/` przez skopiowanie `public/` — `dist/` jest ignorowany przez Git i nie jest tworzony przez `ddev start`.

## GitHub i publikacja automatyczna

Utwórz **puste** repozytorium `devops-basics-2` na GitHub (publiczne, jeśli chcesz publiczne GitHub Pages), a następnie w katalogu projektu:

```bash
git init -b main
git add .
git commit -m "Initial DevOps Basics 2"
git remote add origin git@github.com:TWOJ_LOGIN/devops-basics-2.git
git push -u origin main
```

Jeśli repozytorium masz już zainicjalizowane, nie wykonuj `git init` ponownie; sprawdź `git status` oraz `git remote -v`.

Na GitHub wybierz **Settings → Pages → Build and deployment → Source: GitHub Actions**. Pliki `.github/workflows/ci.yml` oraz `pages.yml` walidują dane, uruchamiają testy, budują `dist/` i wdrażają stronę po `push` na `main`. Docelowy adres to:

```text
https://TWOJ_LOGIN.github.io/devops-basics-2/
```

Skrypty używają tylko Pythona ze standardowej biblioteki. Przykładowe obrazki nie wymagają Pillow podczas budowania (Pillow użyto wyłącznie do przygotowania plików JPEG na etapie tworzenia projektu).

### Aktualizowanie istniejącego DevOps Basics 1

Bezpieczna opcja: **DevOps Basics 2 jest osobnym projektem** (nowy katalog, nowa nazwa DDEV, nowe repozytorium), więc nie nadpisuje dotychczasowego `devops-basics`. Jeśli chcesz zastąpić poprzedni projekt, najpierw utwórz jego kopię i świadomie zdecyduj o nazwie repozytorium oraz URL GitHub Pages.

## Bezpieczeństwo

Nie umieszczaj w JSON, obrazach ani repozytorium prywatnych haseł, tokenów, kluczy SSH czy informacji, których nie chcesz publikować. Wszystkie pliki z `public/`, w tym obrazy, będą publiczne w GitHub Pages.
