# Rozpoczęcie pracy (Getting Started)

**🎓 Dla studentów:** Ten przewodnik pomoże Ci przygotować komputer do pracy z modelami Cosmos. Może wydawać się skomplikowany, ale przejdziemy przez to krok po kroku!

Ten przewodnik obejmuje niezbędne narzędzia i zależności potrzebne do skonfigurowania środowiska deweloperskiego do pracy z modelami Cosmos. Te narzędzia stanowią fundament dla kuratorowania danych, post-treningu modeli, ewaluacji i przepływów pracy wdrożeniowych we wszystkich projektach Cosmos.

---

## Konfiguracja repozytorium (Repository Setup)

**🎓 Co to jest repozytorium?**  
Repozytorium to miejsce gdzie przechowywany jest cały kod projektu. To jak folder, ale z historią wszystkich zmian.

Sklonuj repozytorium Cosmos Cookbook i zainstaluj je w trybie deweloperskim:

```shell
# Sklonuj repozytorium (pobierz kod)
git clone git@github.com:nvidia-cosmos/cosmos-cookbook.git

# Wejdź do katalogu
cd cosmos-cookbook
```

**🎓 Co robi każda komenda:**
- `git clone` - pobiera całe repozytorium na Twój komputer
- `cd cosmos-cookbook` - zmienia aktualny katalog (change directory)

### Struktura Cookbook

**🎓 Zrozumienie organizacji projektu:**

Cosmos Cookbook jest zorganizowany w dwa główne katalogi:

#### 📁 `docs/` - Dokumentacja

Zawiera źródłową dokumentację w plikach markdown:

- **Przewodniki techniczne** - jak używać poszczególnych funkcji
- **Przepływy pracy (workflows)** - kompletne procesy od A do Z
- **Przykłady** - gotowe do uruchomienia case studies
- **Tutoriale** - nauka krok po kroku

**🎓 Markdown (.md):** Prosty format tekstu z formatowaniem. Używany do dokumentacji.

#### 📁 `scripts/` - Kod wykonywany

Zawiera wszystkie wykonywalne skrypty, do których odwołuje się dokumentacja:

- **Przetwarzanie danych** - przygotowanie zbiorów danych do treningu
- **Pipeline'y ewaluacji** - ocena jakości modeli
- **Konfiguracje post-trainingu** - ustawienia dostrajania modeli
- **Narzędzia automatyzacji** - skrypty pomocnicze

**🎓 Dlaczego taki podział?**

```
Typowy przepływ pracy:
1. Czytasz docs/recipes/inference/tutorial.md
2. Widzisz tam: "uruchom scripts/examples/inference.py"
3. Uruchamiasz skrypt
4. Wracasz do dokumentacji po więcej informacji
```

Ta struktura oddziela dokumentację od praktycznej implementacji, ułatwiając nawigację między czytaniem o przepływach pracy a wykonywaniem odpowiednich skryptów.

> **Uwaga:** Te kroki instalacji będą aktualizowane w miarę przygotowywania zewnętrznego repozytorium do publicznego wydania.

---

## Wymagania wstępne (Prerequisites)

**🎓 Wyjaśnienie:** Przed rozpoczęciem musisz sprawdzić czy Twój komputer spełnia wymagania. Cosmos wymaga dużej mocy obliczeniowej!

Przed rozpoczęciem upewnij się, że spełniasz następujące wymagania.

### Sprzęt (Hardware)

**🎓 WAŻNE - Wymagania GPU:**

Do uruchamiania przepisów cookbook i przepływów pracy potrzebujesz:

- **Inferencja (używanie modeli):** minimum 1 GPU
- **Trening (uczenie modeli):** minimum 4 GPU (zalecane 8 GPU)
- **Architektura:** Ampere lub nowsza (A100, H100)

**🎓 Co to jest GPU?**  
GPU (Graphics Processing Unit) to specjalistyczny procesor pierwotnie zaprojektowany do grafiki, ale idealny do AI. Modele AI wykonują miliony obliczeń równolegle - GPU jest w tym tysiące razy szybsze niż zwykły procesor (CPU).

**🎓 Popularne GPU dla AI:**
- **NVIDIA A100** - profesjonalna karta do data center (bardzo droga, ~$10,000)
- **NVIDIA H100** - najnowsza generacja, jeszcze wydajniejsza
- **RTX 4090** - wysokiej klasy karta konsumencka (może działać dla małych modeli)

**🎓 Co jeśli nie mam GPU?**  
Nie martw się! Możesz:
1. Używać chmury (zobacz sekcję "Cloud Deployments" poniżej)
2. Czytać dokumentację i uczyć się teorii
3. Uruchamiać małe przykłady na CPU (będzie wolno, ale zadziała)

Dla szczegółowych wymagań GPU i pamięci dla każdego modelu Cosmos (Predict1, Predict2, Transfer1, etc.), zobacz dokumentację [NVIDIA Cosmos Prerequisites](https://docs.nvidia.com/cosmos/latest/prerequisites.html).

> **Uwaga**: GPU nie jest wymagane do renderowania lokalnej dokumentacji.

### Oprogramowanie (Software)

**🎓 Lista narzędzi które musisz zainstalować:**

- **System operacyjny**: Ubuntu 24.04, 22.04, lub 20.04
  - **🎓 Dlaczego Ubuntu?** To dystrybucja Linuxa z najlepszym wsparciem dla AI/ML
  - **🎓 Czy mogę użyć Windows?** Niestety większość narzędzi AI działa tylko na Linux
  - **🎓 Opcja:** Możesz użyć WSL2 (Windows Subsystem for Linux) na Windows

- **Python**: Wersja 3.10+
  - **🎓 Co to jest Python?** Język programowania, główny język dla AI/ML
  - **🎓 Sprawdź wersję:** `python3 --version`

- **NVIDIA Container Toolkit**: 1.16.2 lub nowszy
  - **🎓 Co to robi?** Pozwala Dockerowi używać GPU
  - **🎓 Bez tego:** Docker nie zobaczy Twojej karty graficznej

- **CUDA**: 12.4 lub nowszy
  - **🎓 Co to jest CUDA?** Platforma NVIDIA do programowania GPU
  - **🎓 Wymagane do:** Uruchamiania obliczeń AI na GPU

- **Docker Engine**
  - **🎓 Co to jest Docker?** System konteneryzacji - jak maszyna wirtualna, ale lżejsza
  - **🎓 Dlaczego?** Zapewnia spójne środowisko (wszystko działa tak samo)

- **Sieć**: Połączenie internetowe do pobierania modeli i zależności
  - **🎓 Rozmiary plików:** Modele AI mogą mieć 10-50 GB!

**🎓 Sprawdzanie instalacji:**

```bash
# Sprawdź system operacyjny
lsb_release -a

# Sprawdź Python
python3 --version

# Sprawdź CUDA
nvcc --version

# Sprawdź Docker
docker --version

# Sprawdź GPU
nvidia-smi
```

---

## Instalacja narzędzi ogólnych (Generic Tool Installation)

**🎓 Wyjaśnienie:** Te narzędzia są potrzebne do zarządzania innymi narzędziami. To jak "narzędzia do zarządzania narzędziami"!

Następujące zależności systemowe są wymagane do uruchomienia Cosmos Cookbook:

### pkgx

**🎓 Co to jest pkgx?**  
pkgx to nowoczesny menedżer pakietów, który upraszcza instalację i zarządzanie narzędziami CLI. Zapewnia izolowane środowiska i automatyczne rozwiązywanie zależności.

**🎓 Dlaczego nie apt/yum?**  
- pkgx jest szybszy i prostszy
- Automatycznie zarządza wersjami
- Nie wymaga uprawnień sudo dla większości rzeczy

[pkgx](https://docs.pkgx.sh/) - dokumentacja

```shell
# Instalacja przez brew (jeśli masz) LUB przez skrypt instalacyjny
brew install pkgx || curl https://pkgx.sh | sh
```

**🎓 Co robi ta komenda:**
- `brew install pkgx` - próbuje zainstalować przez Homebrew
- `||` - "lub" - jeśli pierwsze się nie uda, spróbuj drugiego
- `curl https://pkgx.sh | sh` - pobierz i uruchom skrypt instalacyjny

### uv

**🎓 Co to jest uv?**  
uv to szybki instalator i resolver pakietów Python, zaprojektowany jako zamiennik dla pip. Jest niezbędny do zarządzania zależnościami Python w projektach Cosmos.

**🎓 pip vs uv:**
- **pip** - tradycyjny menedżer pakietów Python (wolniejszy)
- **uv** - nowoczesna alternatywa (10-100x szybsza!)

[uv](https://docs.astral.sh/uv/) - dokumentacja

```shell
pkgm install uv
```

**🎓 Co robi ta komenda:**
Instaluje uv używając pkgm (część pkgx)

### Hugging Face CLI

**🎓 Co to jest Hugging Face?**  
Hugging Face to "GitHub dla modeli AI". To platforma gdzie znajdują się tysiące gotowych modeli AI, które możesz pobrać i użyć.

**🎓 Dlaczego potrzebujemy CLI?**  
CLI (Command Line Interface) pozwala pobrać modele bezpośrednio z terminala, bez ręcznego pobierania przez przeglądarkę.

[Hugging Face CLI](https://huggingface.co/docs/huggingface_hub/en/guides/cli) jest niezbędne do pobierania wytrenowanych checkpointów modeli i zbiorów danych z Hugging Face Hub.

```shell
# Instalacja
pkgm install huggingface-cli

# Logowanie (potrzebne do pobierania modeli)
huggingface-cli login
```

**🎓 Proces logowania:**
1. Uruchom `huggingface-cli login`
2. Poprosi Cię o token
3. Idź na https://huggingface.co/settings/tokens
4. Utwórz nowy token (read access wystarczy)
5. Skopiuj i wklej token

> **Uwaga**: Potrzebujesz konta Hugging Face i tokenu dostępu do uwierzytelniania.

**🎓 Dlaczego token jest bezpieczny?**  
Token działa jak hasło, ale możesz je odwołać w dowolnym momencie. Nigdy nie podawaj swojego głównego hasła do skryptów.

---

## Szybki start wdrożeń w chmurze (Cloud Deployments Quick Start)

**🎓 Co to jest wdrożenie w chmurze?**  
Zamiast używać własnego komputera, wynajmujesz moc obliczeniową w internecie. To jak Netflix dla GPU - płacisz za użycie, nie musisz kupować sprzętu.

**🎓 Kiedy używać chmury:**
- ✅ Nie masz odpowiedniego GPU
- ✅ Chcesz szybko przetestować
- ✅ Potrzebujesz dużo mocy na krótki czas
- ✅ Nie chcesz konfigurować środowiska

**🎓 Wady chmury:**
- ❌ Kosztuje (ale często mniej niż zakup GPU)
- ❌ Potrzebujesz dobrego internetu
- ❌ Dane są "w chmurze" (kwestia prywatności)

Te przewodniki wdrożeń w chmurze pomogą Ci wdrożyć i uruchomić modele Cosmos bez lokalnej konfiguracji infrastruktury.

### Dostępne opcje chmurowe:

#### Brev - Platforma GPU w chmurze

**🎓 Co to jest Brev?**  
Brev to platforma oferująca łatwy dostęp do GPU w chmurze. Kliknij kilka przycisków i masz działający serwer z GPU!

- **[Rozpocznij z Cosmos Reason1 na Brev](brev/reason1/reason1_on_brev.md)** 
  - Wdrożenie Cosmos Reason1 do rozumowania Physical AI
  - Ten przewodnik obejmuje provisioning, konfigurację i pierwszą inferencję
  - **🎓 Dla kogo:** Świetne do eksperymentowania z analizą wideo

- **[Rozpocznij z Transfer2.5 i Predict2.5 na Brev](brev/transfer2_5/transfer_and_predict_on_brev.md)** 
  - Konfiguracja Transfer2.5 (generowanie wideo) i Predict2.5 (predykcja świata)
  - Infrastruktura Brev cloud z przykładowymi przepływami pracy
  - **🎓 Dla kogo:** Jeśli chcesz generować lub przekształcać wideo

**🎓 Typowe koszty (orientacyjnie):**
- GPU klasy A100: ~$2-4 za godzinę
- Tip: Zatrzymuj instancję gdy nie używasz!
- Wiele platform oferuje darmowe kredyty na start

---

## 🎓 Podsumowanie dla studentów

### Sprawdzenie gotowości:

**Poziom 1: Czytanie dokumentacji (każdy)**
- ✅ Komputer z przeglądarką
- ✅ Połączenie internetowe
- ✅ Ciekawość i chęć nauki!

**Poziom 2: Uruchamianie małych przykładów (studenci)**
- ✅ Linux (Ubuntu zalecane)
- ✅ Python 3.10+
- ✅ Podstawowa znajomość terminala

**Poziom 3: Pełne przepływy pracy (zaawansowani)**
- ✅ GPU (własne lub w chmurze)
- ✅ CUDA i Docker
- ✅ Znajomość Git i Python

### Ścieżka nauki:

```mermaid
1. Czytaj dokumentację
   ↓
2. Eksperymentuj z małymi przykładami (CPU)
   ↓
3. Spróbuj chmury (darmowy kredyt)
   ↓
4. Rozważ własne GPU (gdy wiesz że będziesz używać)
```

### Następne kroki:

1. **[README.md](../../README.md)** - Przegląd całego projektu
2. **[CONTRIBUTING_PL.md](../../CONTRIBUTING_PL.md)** - Jak współtworzyć
3. **Recipes (Przepisy)** - Wypróbuj pierwszy przepis!

### Potrzebujesz pomocy?

- **GitHub Issues:** Zadaj pytanie w Issues
- **Dokumentacja:** Zawsze czytaj najpierw dokumentację
- **Community:** Społeczność jest przyjazna!

**Pamiętaj:** Każdy ekspert kiedyś był początkującym. Zadawaj pytania, eksperymentuj i ucz się! 🚀

---

## Dodatkowe zasoby

### Kursy online (darmowe):
- **fast.ai** - Praktyczny deep learning
- **Hugging Face Course** - Uczenie się NLP i transformerów
- **CUDA Programming** - Programowanie GPU

### Książki:
- "Deep Learning" by Ian Goodfellow
- "Hands-On Machine Learning" by Aurélien Géron

### YouTube:
- 3Blue1Brown - Wizualizacje AI
- Two Minute Papers - Najnowsze badania AI
- Yannic Kilcher - Szczegółowe omówienia papers

**Powodzenia w nauce! 🎓✨**
