# Cosmos Cookbook (Książka kucharska Cosmos)

[![Dokumentacja](https://img.shields.io/badge/docs-cosmos--cookbook-blue)](https://nvidia-cosmos.github.io/cosmos-cookbook/)
[![Przewodnik współtworzenia](https://img.shields.io/badge/contributing-guide-green)](CONTRIBUTING.md)

Kompleksowy przewodnik do pracy z **ekosystemem NVIDIA Cosmos**—zestawem modeli fundamentowych świata (World Foundation Models - WFMs) dla rzeczywistych, specyficznych dla domeny zastosowań w robotyce, symulacji, systemach autonomicznych i rozumieniu scen fizycznych.

**📚 [Zobacz pełną dokumentację →](https://nvidia-cosmos.github.io/cosmos-cookbook/)** — Przepływy pracy krok po kroku, studia przypadków i przepisy techniczne

---

## 🎓 Dla studentów i osób uczących się

Ten projekt jest idealny dla studentów i początkujących, którzy chcą nauczyć się AI fizycznego (Physical AI). **NVIDIA Cosmos** to zestaw zaawansowanych modeli sztucznej inteligencji, które potrafią:

- **Rozumieć i generować wideo** - tworzenie realistycznych sekwencji wideo na podstawie opisów tekstowych
- **Przewidywać przyszłość** - symulowanie tego, co może się wydarzyć w świecie fizycznym
- **Rozumować o świecie fizycznym** - odpowiadanie na pytania o to, co dzieje się na wideo lub obrazach
- **Przetwarzać i kuratorować dane wideo** - przygotowywanie dużych zbiorów danych do treningu modeli

**Co wyróżnia ten przewodnik?**
- Szczegółowe wyjaśnienia krok po kroku
- Komentarze w kodzie wyjaśniające "dlaczego", a nie tylko "jak"
- Przykłady z życia wzięte (roboty, samochody autonomiczne, magazyny)
- Gotowe przepisy (recipes), które możesz uruchomić i modyfikować

<https://github.com/user-attachments/assets/bb444b93-d6af-4e25-8bd0-ca5891b26276>

---

## Najnowsze aktualizacje (Latest Updates)

| **Data** | **Przepis (Recipe)** | **Model** | **Opis** |
|----------|------------|-----------|-----------------|
| 4 lut | [Bezpieczeństwo pracowników w klasycznym magazynie](https://nvidia-cosmos.github.io/cosmos-cookbook/recipes/inference/reason2/worker_safety/inference.html) | Cosmos Reason 2 | Wykrywanie zagrożeń i zgodności z przepisami BHP w środowisku magazynowym bez wcześniejszego treningu (zero-shot) |
| 30 sty | [Przewodnik po promptach](https://nvidia-cosmos.github.io/cosmos-cookbook/core_concepts/prompt_guide/reason_guide.html) | Cosmos Reason 2 | Jak efektywnie pisać zapytania do modelu |
| 29 sty | [Wyszukiwanie i podsumowywanie wideo z Cosmos Reason](https://nvidia-cosmos.github.io/cosmos-cookbook/recipes/inference/reason2/vss/inference.html) | Cosmos Reason 2 | Przyśpieszona na GPU analiza dużych zbiorów wideo dla magazynów, fabryk i smart city |
| 28 sty | [Cosmos Policy: Dostrajanie modeli wideo dla kontroli wizuomotorycznej](https://nvidia-cosmos.github.io/cosmos-cookbook/recipes/post_training/predict2/cosmos_policy/post_training.html) | Cosmos Predict 2 | Zaawansowany model polityki robota osiągający 98.5% skuteczności na LIBERO |
| 27 sty | [Przewidywanie wiarygodności fizycznej z Cosmos Reason 2](https://nvidia-cosmos.github.io/cosmos-cookbook/recipes/post_training/reason2/physical-plausibility-check/post_training.html) | Cosmos Reason 2 | Trenowanie nadzorowane do przewidywania, czy zjawisko na wideo jest fizycznie możliwe |
| 26 sty | [Post-trening transportu inteligentnego z Cosmos Reason 2](https://nvidia-cosmos.github.io/cosmos-cookbook/recipes/post_training/reason2/intelligent-transportation/post_training.html) | Cosmos Reason 2 | Dostrajanie modelu do rozumienia scen drogowych |

## Nadchodzące wydarzenia (Upcoming Activities)

### NVIDIA GTC 2026

Zarejestruj się na [NVIDIA GTC](https://www.nvidia.com/gtc/) odbywającą się **16–19 marca 2026** i dodaj [sesje Cosmos](https://www.nvidia.com/gtc/session-catalog/?sessions=S81667,CWES81669,DLIT81644,DLIT81698,S81836,S81488,S81834,DLIT81774,CWES81733,CWES81568) do swojego kalendarza. Nie przegap keynote CEO Jensena Huanga w SAP Center w poniedziałek 16 marca o 11:00 czasu pacyficznego.

### NVIDIA Cosmos Cookoff

Przedstawiamy **[NVIDIA Cosmos Cookoff](https://luma.com/nvidia-cosmos-cookoff)** — wirtualny, czterotygodniowy konkurs Physical AI trwający **29 stycznia – 26 lutego** dla twórców robotyki, pojazdów autonomicznych i AI wizyjnego.

Buduj z NVIDIA Cosmos Reason i przepisami Cosmos Cookbook—od rozumowania egocentrycznego robotów po sprawdzanie wiarygodności fizycznej i modele świadome ruchu drogowego, aby wygrać **$5,000**, **NVIDIA DGX Spark** i więcej!

**[Zarejestruj się teraz →](https://luma.com/nvidia-cosmos-cookoff)**

Sponsorowane przez Nebius i Milestone.

## Wymagania wstępne (Prerequisites)

**🎓 Wyjaśnienie dla studentów:**  
Przed rozpoczęciem pracy z Cosmos, musisz przygotować odpowiednie środowisko. Cosmos używa zaawansowanych modeli AI, które wymagają dużej mocy obliczeniowej (GPU), dlatego lista wymagań może wydawać się skomplikowana. Poniżej wyjaśniamy, czego potrzebujesz.

| Przypadek użycia | Linux (Ubuntu) | macOS | Windows |
|----------|----------------|-------|---------|
| Uruchamianie przepisów (GPU workflows) | ✅ Wspierane | ❌ | ❌ |
| Lokalna dokumentacja i współtworzenie | ✅ Wspierane | ✅ Wspierane | ⚠️ WSL zalecane |

### Dla dokumentacji i współtworzenia (wszystkie platformy)

- **Git** z [Git LFS](#1-zainstaluj-git-lfs-wymagane)
- **Python**: Wersja 3.10 lub nowsza
- **Dostęp do internetu** do klonowania i pobierania zależności

### Dla uruchamiania przepisów Cookbook (tylko Ubuntu)

Pełne przepływy pracy GPU wymagają środowiska Ubuntu Linux z kartami graficznymi NVIDIA.

→ Zobacz **[Rozpoczęcie pracy](https://nvidia-cosmos.github.io/cosmos-cookbook/getting_started/setup.html)** dla pełnych wymagań sprzętowych i programowych.

→ Lub **[Wdrożenie w chmurze](https://nvidia-cosmos.github.io/cosmos-cookbook/getting_started/cloud_platform.html)** (Nebius, Brev i więcej wkrótce) dla gotowych instancji GPU.

## Szybki start (Quick Start)

### 1. Zainstaluj Git LFS (Wymagane)

**🎓 Wyjaśnienie:** Git LFS (Large File Storage) to rozszerzenie Git, które pozwala efektywnie zarządzać dużymi plikami (wideo, obrazy). W tym repozytorium są setki plików wideo demonstracyjnych, więc Git LFS jest **niezbędne**.

> ⚠️ **Ważne**: To repozytorium zawiera wiele plików multimedialnych (wideo, obrazy, demonstracje). Git LFS jest **wymagane** do prawidłowego klonowania i pracy z tym repozytorium.

```bash
# Ubuntu/Debian (zalecane)
sudo apt update && sudo apt install git-lfs

# Włącz Git LFS globalnie
git lfs install
```

Dla innych platform (macOS, Windows, Fedora), zobacz oficjalny przewodnik instalacji na **[git-lfs.com](https://git-lfs.com/)**.

Jeśli już sklonowałeś repozytorium bez LFS, pobierz pliki multimedialne za pomocą:

```bash
git lfs pull
```

### 2. Zainstaluj zależności systemowe

**🎓 Wyjaśnienie:** 
- **uv** - szybki menedżer pakietów Python (alternatywa dla pip), który przyspiesza instalację bibliotek
- **just** - narzędzie do uruchamiania poleceń (podobne do make), które ułatwia wykonywanie typowych zadań

```bash
# Zainstaluj uv (szybki menedżer pakietów Python)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

# Zainstaluj just (narzędzie do uruchamiania poleceń)
uv tool install -U rust-just
```

Dla innych platform zobacz **[astral.sh/uv](https://astral.sh/uv/)** dla instrukcji instalacji.

### 3. Sklonuj i skonfiguruj repozytorium

**🎓 Wyjaśnienie:** Ten krok pobiera całe repozytorium na Twój komputer i instaluje wszystkie potrzebne biblioteki Python.

```bash
# Sklonuj repozytorium
git clone https://github.com/nvidia-cosmos/cosmos-cookbook.git
cd cosmos-cookbook

# Zainstaluj zależności i skonfiguruj środowisko
just install
```

### 4. Przeglądaj dokumentację

**🎓 Wyjaśnienie:** Możesz otworzyć dokumentację lokalnie w przeglądarce, co pozwala na czytanie offline i szybsze przeglądanie.

```bash
# Uruchom dokumentację lokalnie
just serve-external  # Dla dokumentacji publicznej
# lub
just serve-internal   # Dla dokumentacji wewnętrznej (jeśli dotyczy)
```

Następnie otwórz [http://localhost:8000](http://localhost:8000) w przeglądarce.

## Struktura repozytorium (Repository Structure)

**🎓 Wyjaśnienie:** Repozytorium jest podzielone na dwie główne części: dokumentację (`docs/`) i kod (`scripts/`). To ułatwia naukę - możesz najpierw przeczytać o tym, jak coś działa, a potem zobaczyć kod implementacji.

Cosmos Cookbook jest zorganizowany w dwa główne katalogi:

### `docs/`

Zawiera źródłową dokumentację w plikach markdown:

- **Przewodniki techniczne** - szczegółowe wyjaśnienia jak działają poszczególne komponenty
- **Przykłady end-to-end** - kompletne przypadki użycia od początku do końca
- **Przepisy krok po kroku** - gotowe do uruchomienia przykłady
- **Przewodniki startowe** - pomoc w rozpoczęciu pracy

### `scripts/`

Zawiera wykonywalne skrypty, do których odwołuje się dokumentacja:

- **Przetwarzanie i kuratorowanie danych** - przygotowanie zbiorów danych do treningu
- **Ewaluacja modeli** - skrypty do oceny jakości modeli
- **Konfiguracje post-trainingu** - pliki konfiguracyjne do dostrajania modeli
- **Narzędzia automatyzacji** - utility do automatyzacji powtarzalnych zadań

Ta struktura oddziela dokumentację od implementacji, ułatwiając nawigację między czytaniem o przepływach pracy a wykonywaniem odpowiednich skryptów.

## Wskazówki dotyczące plików multimedialnych (Media File Guidelines)

**🎓 Wyjaśnienie:** Jeśli będziesz dodawać własne materiały wideo do projektu, ważne jest, aby używać odpowiedniego formatu.

Podczas dodawania plików multimedialnych, preferuj `.mp4` zamiast `.gif`:

- **Lepsza jakość** — MP4 wspiera pełną głębię kolorów vs limit 256 kolorów w GIF
- **Mniejszy rozmiar pliku** — Nowoczesne kodeki wideo kompresują znacznie efektywniej
- **Wsparcie dla audio** — MP4 może zawierać narrację gdy potrzeba

Używaj kodowania **H.264** dla uniwersalnej kompatybilności z przeglądarkami.

## Dostępne polecenia (Available Commands)

**🎓 Wyjaśnienie:** Narzędzie `just` pozwala uruchamiać często używane polecenia za pomocą prostych komend. Poniżej znajdują się najważniejsze polecenia, których będziesz używać.

```bash
# Rozwój (Development)
just install          # Zainstaluj zależności i skonfiguruj środowisko
just setup            # Skonfiguruj hooki pre-commit (sprawdzanie kodu przed commitem)
just serve-external   # Uruchom publiczną dokumentację lokalnie
just serve-internal   # Uruchom wewnętrzną dokumentację lokalnie

# Kontrola jakości (Quality Control)
just lint            # Uruchom sprawdzanie i formatowanie kodu
just test            # Uruchom wszystkie testy i walidację

# Ciągła integracja (Continuous Integration)
just ci-lint         # Uruchom sprawdzanie CI lintingu
just ci-deploy-internal         # Wdróż dokumentację wewnętrzną
just ci-deploy-external         # Wdróż dokumentację zewnętrzną
```

## Współtworzenie i wsparcie (Contributing & Support)

**🎓 Wyjaśnienie:** Cosmos Cookbook to projekt open-source, co oznacza, że każdy może współtworzyć i ulepszać ten projekt. Jeśli znajdziesz błąd, masz pomysł na ulepszenie lub chcesz dodać własny przepis - jesteś mile widziany!

- **[Przewodnik współtworzenia](CONTRIBUTING.md)** - Jak współtworzyć cookbook
- **Zgłaszanie problemów**: Użyj [GitHub Issues](https://github.com/nvidia-cosmos/cosmos-cookbook/issues) dla błędów i próśb o nowe funkcje
- **Dziel się sukcesami**: Uwielbiamy słyszeć o kreatywnych zastosowaniach modeli Cosmos

## Licencja i kontakt (License and Contact)

**🎓 Wyjaśnienie:** 
- **Licencja** określa, jak możesz używać tego oprogramowania
- **Apache 2 License** to licencja open-source pozwalająca na swobodne użycie, modyfikację i dystrybucję kodu
- **NVIDIA Open Model License** reguluje użycie samych modeli AI

Ten projekt pobierze i zainstaluje dodatkowe projekty open source innych firm. Przejrzyj warunki licencji tych projektów przed użyciem.

Kod źródłowy NVIDIA Cosmos jest wydany na licencji [Apache 2 License](https://www.apache.org/licenses/LICENSE-2.0).

Modele NVIDIA Cosmos są wydane na licencji [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license). W sprawie niestandardowej licencji skontaktuj się z [cosmos-license@nvidia.com](mailto:cosmos-license@nvidia.com).
