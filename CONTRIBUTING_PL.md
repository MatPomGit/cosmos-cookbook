# Współtworzenie Cosmos Cookbook (Contributing)

**🎓 Dla studentów:** Ten dokument wyjaśnia jak możesz pomóc w rozwoju projektu Cosmos Cookbook. Współtworzenie projektów open-source to świetny sposób na naukę i zdobycie doświadczenia!

Cosmos Cookbook to zasób tworzony przez społeczność, służący do dzielenia się praktyczną wiedzą o ekosystemie NVIDIA Cosmos. Zapraszamy do współtworzenia, w tym przepływów pracy, przepisów, najlepszych praktyk i adaptacji specyficznych dla domeny.

---

## Co możesz dodać (What to Contribute)

**🎓 Wyjaśnienie:** Istnieje wiele sposobów, w jakie możesz pomóc - nie musisz być ekspertem!

### Przepisy (Recipes)
Przewodniki krok po kroku dla:
- **Inferencja** - używanie gotowych modeli (łatwiejsze, dobry start!)
- **Post-training** - dostrajanie modeli (fine-tuning, LoRA, adaptacja domenowa)

**🎓 Przykład:** "Jak używać Cosmos Reason do analizy wideo z magazynu"

### Koncepcje (Concepts)
Wyjaśnienia fundamentalnych tematów:
- Techniki i wzorce architektoniczne
- Dokumentacja narzędzi
- Najlepsze praktyki

**🎓 Przykład:** "Co to jest inferencja i jak działa?"

### Ulepszenia (Improvements)
- Poprawki błędów
- Aktualizacje dokumentacji
- Naprawianie niedziałających linków
- Wyjaśnianie niejasnych fragmentów

**🎓 Dla początkujących:** Zacznij od małych rzeczy - znajdź literówkę lub niejasne zdanie i zaproponuj poprawkę!

---

## Jak współtworzyć (How to Contribute)

**🎓 Wyjaśnienie pojęć Git:**
- **Fork** - twoja własna kopia projektu
- **Branch** - oddzielna "gałąź" dla Twoich zmian
- **Pull Request (PR)** - prośba o włączenie Twoich zmian do głównego projektu
- **Issue** - zgłoszenie problemu lub pomysłu

### Metody współtworzenia:

- **Pull Request** - Dla kompletnych wkładów (użyj draft PR dla prac w toku)
- **Issue** - Dla propozycji, pomysłów lub zgłaszania braków w dokumentacji

---

## Przepływ pracy (Contribution Workflow)

### 1. Fork i konfiguracja

**🎓 Co to znaczy "fork"?**  
Fork to Twoja własna kopia projektu na GitHubie. Możesz w niej swobodnie eksperymentować bez wpływu na oryginalny projekt.

Zrób fork [repozytorium Cosmos Cookbook](https://github.com/nvidia-cosmos/cosmos-cookbook), następnie sklonuj i skonfiguruj:

```bash
# Sklonuj swoją kopię (fork)
git clone https://github.com/YOUR-USERNAME/cosmos-cookbook.git
cd cosmos-cookbook

# Dodaj link do oryginalnego repozytorium (upstream)
# Dzięki temu możesz pobierać najnowsze zmiany
git remote add upstream https://github.com/nvidia-cosmos/cosmos-cookbook.git

# Zainstaluj zależności (szczegóły w README)
just install

# Sprawdź czy działa
just serve-internal  # Odwiedź http://localhost:8000
```

**🎓 Co robi każda komenda:**
- `git clone` - pobiera kod na Twój komputer
- `git remote add upstream` - dodaje link do oryginalnego projektu
- `just install` - instaluje wszystkie potrzebne biblioteki
- `just serve-internal` - uruchamia lokalną wersję dokumentacji

### 2. Utwórz branch (gałąź)

**🎓 Dlaczego tworzymy branch?**  
Branch to oddzielna "gałąź" projektu. Pracujesz w niej nad swoimi zmianami, nie psując głównej wersji (main).

```bash
git checkout -b recipe/opisowa-nazwa  # lub docs/, fix/, etc.
```

**🎓 Konwencje nazewnictwa:**
- `recipe/` - dla nowych przepisów
- `docs/` - dla dokumentacji
- `fix/` - dla poprawek błędów
- Używaj opisowych nazw: `recipe/traffic-analysis` zamiast `recipe/my-changes`

### 3. Wprowadź zmiany

**🎓 Proces tworzenia:**
1. Edytuj pliki (markdown, Python, etc.)
2. Zapisz zmiany
3. Przetestuj czy działają

Dodaj swoją treść zgodnie z szablonami poniżej, następnie przetestuj:

```bash
# Podgląd zmian w przeglądarce
just serve-internal  # Otwórz http://localhost:8000

# Uruchom walidację (sprawdzenie poprawności)
just test
```

**🎓 Podgląd Twojego przepisu lokalnie:**

Po uruchomieniu `just serve-internal`, otwórz przeglądarkę i przejdź do:

- **Strona główna:** `http://localhost:8000`
- **Twój przepis:** `http://localhost:8000/recipes/[kategoria]/[nazwa-modelu]/[nazwa-przepisu]/`

**Przykład:**  
Jeśli dodałeś przepis w `docs/recipes/inference/transfer2_5/my-new-recipe/inference.md`, zobaczysz go pod:
`http://localhost:8000/recipes/inference/transfer2_5/my-new-recipe/inference/`

Lokalny serwer automatycznie przeładowuje się gdy zapiszesz zmiany w plikach markdown.

### 4. Commit i Push

**🎓 Co to jest commit?**  
Commit to "migawka" Twoich zmian z opisem co zrobiłeś. To jak punkt kontrolny w grze.

```bash
# Dodaj wszystkie zmienione pliki
git add .

# Utwórz commit z opisem (w języku angielskim dla spójności projektu)
git commit -m "Add Transfer weather augmentation recipe"

# Wyślij zmiany do Twojego forka na GitHub
git push origin recipe/opisowa-nazwa
```

**🎓 Dobre praktyki commitów:**
- Pisz jasne opisy co zmieniłeś
- Jeden commit = jedna logiczna zmiana
- Używaj czasu teraźniejszego: "Add" zamiast "Added"

### 5. Utwórz Pull Request (PR)

**🎓 Co to jest Pull Request?**  
Pull Request (PR) to formalna prośba o włączenie Twoich zmian do głównego projektu. Maintainerzy (opiekunowie projektu) przejrzą Twój kod i mogą poprosić o poprawki.

1. Odwiedź swój fork na GitHubie i kliknij **"Compare & pull request"**
2. Wypełnij szablon PR z jasnym tytułem i opisem
3. Połącz powiązane issues używając `Closes #123` lub `Relates to #456`
4. Prześlij PR do recenzji

**🎓 Co napisać w opisie PR:**
- Co dodałeś/zmieniłeś
- Dlaczego to jest potrzebne
- Jak to przetestowałeś
- Zrzuty ekranu (jeśli dotyczy)

### 6. Odpowiedz na feedback

**🎓 Proces review:**  
Maintainerzy przejrzą Twój kod i mogą zostawić komentarze z sugestiami. To normalne i pomocne - wszyscy się uczymy!

Zaktualizuj swój branch na podstawie komentarzy recenzji:

```bash
# Wprowadź poprawki w plikach
# Następnie:
git add .
git commit -m "Address review feedback"
git push origin recipe/opisowa-nazwa
```

**🎓 Dobre praktyki:**
- Odpowiadaj na komentarze uprzejmie
- Zadawaj pytania jeśli czegoś nie rozumiesz
- Bądź otwarty na sugestie - to okazja do nauki!

PR aktualizuje się automatycznie. Po zatwierdzeniu, maintainerzy włączą Twój wkład.

### 7. Po włączeniu PR

**🎓 Gratulacje! Jesteś oficjalnym współtwórcą projektu open-source! 🎉**

Co się dzieje dalej:

1. **Twoja treść jest online** - Zmiany są automatycznie wdrażane na [stronę Cosmos Cookbook](https://nvidia-cosmos.github.io/cosmos-cookbook/) w ciągu kilku minut
2. **Aktualizacje indeksu** - Jeśli nie zaktualizowałeś plików indeksowych (`docs/index.md`, `README.md`, `docs/recipes/all_recipes.md`), maintainerzy dodadzą Twój wkład do tych plików w kolejnym commicie
3. **Świętuj!** 🎉 - Twój wkład jest teraz częścią bazy wiedzy społeczności Cosmos

**Następne kroki:**

- Podziel się swoim przepisem ze społecznością
- Rozważ dodanie kolejnych przepisów lub ulepszeń
- Pomóż w recenzji innych wkładów społeczności

**🎓 Dodaj to do CV:**  
Współtworzenie projektów open-source to cenna umiejętność ceniona przez pracodawców!

### Synchronizuj swój Fork

**🎓 Dlaczego synchronizować?**  
Oryginalny projekt ciągle się rozwija. Musisz pobrać najnowsze zmiany zanim zaczniesz nową pracę, aby uniknąć konfliktów.

Przed rozpoczęciem nowej pracy:

```bash
# Przejdź do głównej gałęzi
git checkout main

# Pobierz zmiany z oryginalnego projektu
git fetch upstream

# Włącz je do swojej kopii
git merge upstream/main

# Wyślij zaktualizowaną wersję do swojego forka
git push origin main
```

**🎓 Kiedy to robić:**
- Przed rozpoczęciem każdej nowej pracy
- Co jakiś czas, aby być na bieżąco
- Jeśli widzisz komunikat o "conflicting changes"

---

## Szablony treści i organizacja (Content Templates and Organization)

### Struktura katalogów

**🎓 Wyjaśnienie:** Projekt jest zorganizowany w logiczne sekcje. Musisz wiedzieć gdzie umieścić swoją pracę.

Cosmos Cookbook jest podzielony na trzy główne obszary treści:

#### 1. **Getting Started** (`docs/getting_started/`)

**🎓 Przeznaczenie:** Dokumenty pomocnicze, które pomagają użytkownikom szybko rozpocząć pracę z modelami Cosmos.

**Używaj do:**
- Przewodników instalacji i konfiguracji
- Szybkich tutoriali
- Przewodników wdrażania specyficznych dla platformy (np. Brev, platformy chmurowe)
- Wymagań wstępnych i konfiguracji środowiska

**🎓 Przykład:** "Jak zainstalować Cosmos na swoim komputerze"

#### 2. **Core Concepts** (`docs/core_concepts/`)

**🎓 Przeznaczenie:** Treści dydaktyczne wyjaśniające fundamentalne tematy, techniki i wzorce architektoniczne.

**Używaj do:**
- Wyjaśnień kluczowych koncepcji i technik
- Szczegółowych analiz architektury
- Najlepszych praktyk i wytycznych
- Dokumentacji technicznej referencyjnej

**🎓 Przykład:** "Jak działa model transformera w Cosmos Reason"

**Struktura:**

```
docs/core_concepts/
├── [kategoria]/                # np. data_curation, post_training, evaluation
│   ├── overview.md            # Przegląd kategorii
│   ├── [temat].md             # Indywidualne przewodniki koncepcyjne
│   └── assets/                # Multimedia pomocnicze
```

**Przykładowe kategorie:** `data_curation`, `post_training`, `control_modalities`, `evaluation`, `distillation`

#### 3. **Recipes** (`docs/recipes/`)

**🎓 Przeznaczenie:** Praktyczne przewodniki krok po kroku demonstrujące rzeczywiste aplikacje i przepływy pracy.

**Używaj do:**
- Przepływów pracy inferencji używających wytrenowanych modeli
- Przewodników post-trainingu/dostrajania
- Przepływów pracy end-to-end
- Pipeline'ów kuratorowania danych

**🎓 Przykład:** "Jak użyć Cosmos Transfer do augmentacji wideo pogodowego"

**Struktura:**

```
docs/recipes/
├── inference/                  # Przepływy pracy inferencji
│   └── [nazwa-modelu]/        # np. predict2, transfer2_5, reason1
│       └── [nazwa-przepisu]/
│           ├── inference.md   # Główna treść
│           ├── setup.md       # Opcjonalny przewodnik konfiguracji
│           └── assets/        # Media i konfiguracje
├── post_training/             # Przepływy pracy treningu/dostrajania
│   └── [nazwa-modelu]/
│       └── [nazwa-przepisu]/
│           ├── post_training.md
│           ├── setup.md
│           └── assets/
├── data_curation/             # Pipeline'y przetwarzania danych
│   └── [nazwa-przepisu]/
│       ├── data_curation.md
│       └── assets/
└── end2end/                   # Kompletne przepływy pracy
    └── [nazwa-przepływu]/
        ├── workflow_e2e.md
        └── assets/
```

### Szablony treści

**🎓 Wyjaśnienie:** Szablony to gotowe struktury dokumentów. Używaj ich aby Twoja praca była spójna z resztą projektu.

Użyj odpowiedniego szablonu dla swojego wkładu:

- [Szablon przepisu inferencji](assets/templates/inference_template.md) - Aplikacje wytrenowanych modeli
- [Szablon przepisu post-trainingu](assets/templates/post_training_template.md) - Dostrajanie i adaptacja domenowa
- [Szablon koncepcji](assets/templates/concept_template.md) - Przewodniki wyjaśniające na tematy fundamentalne

**🎓 Jak używać szablonów:**
1. Otwórz odpowiedni szablon
2. Skopiuj strukturę
3. Wypełnij swoją treścią
4. Dostosuj do swoich potrzeb

---

## Wytyczne (Guidelines)

**🎓 Ważne zasady współpracy:**

### Licencjonowanie zbiorów danych
Sprawdź odpowiednie licencjonowanie dla wszystkich używanych zbiorów danych. Dołącz jasne informacje o atrybucji i licencji.

**🎓 Dlaczego to ważne:**  
Niektóre zbiory danych mają ograniczenia użycia. Musisz respektować prawa autorów.

### Recenzja kodu
Wszystkie zgłoszenia wymagają recenzji (zazwyczaj w ciągu tygodnia). Odpowiadaj na feedback szybko i utrzymuj dyskusje profesjonalne.

**🎓 Etykieta recenzji:**
- Bądź uprzejmy
- Przyjmuj krytykę konstruktywnie
- Zadawaj pytania jeśli czegoś nie rozumiesz
- Dziękuj za sugestie

---

## Developer Certificate of Origin (Opcjonalne)

**🎓 Co to znaczy?**  
To formalne oświadczenie, że masz prawo do przesłania swojego wkładu i zgadzasz się na licencję projektu.

Możesz opcjonalnie podpisać swoje commity używając `git commit -s`, co dodaje `Signed-off-by: Your Name <your@email.com>` do Twojej wiadomości commit.

Podpisując, potwierdzasz że masz prawo przesłać wkład na licencji open source projektu, zgodnie z [Developer Certificate of Origin 1.1](https://developercertificate.org/).

**🎓 Kiedy używać:**
- Jeśli Twoja organizacja tego wymaga
- Dla formalnego potwierdzenia praw autorskich
- Nie jest wymagane dla większości wkładów

---

## 🎓 Podsumowanie dla początkujących

### Najłatwiejsze sposoby na start:

1. **Znajdź literówkę** - Przeczytaj dokumentację i zgłoś lub napraw błędy
2. **Dodaj wyjaśnienie** - Jeśli coś nie było dla Ciebie jasne, dodaj wyjaśnienie
3. **Przetłumacz** - Pomóż w tłumaczeniu na inne języki
4. **Dodaj przykład** - Dodaj prosty przykład użycia
5. **Udoskonal dokumentację** - Dodaj zrzuty ekranu lub diagramy

### Zasoby pomocnicze:

- **Git tutorial:** [https://git-scm.com/docs/gittutorial](https://git-scm.com/docs/gittutorial)
- **Markdown guide:** [https://www.markdownguide.org/](https://www.markdownguide.org/)
- **GitHub docs:** [https://docs.github.com/](https://docs.github.com/)

### Potrzebujesz pomocy?

- Otwórz Issue z pytaniem
- Poproś o pomoc w opisie PR
- Społeczność jest przyjazna i chętnie pomoże!

**Pamiętaj:** Każdy ekspert kiedyś był początkującym. Nie bój się zadawać pytań i popełniać błędów - to część procesu nauki! 🚀
