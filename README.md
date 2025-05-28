# 🧮 MAE — Modular Arithmetic Engine & 💬 CriptoChat

    

> **Mathematics, Algorithms & Encryption in pure Python** — a fast number‑theory toolbox (MAE) powering an RSA‑based command‑line messenger (CriptoChat).

---

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Highlights](#highlights)
3. [Algorithms in the Engine](#algorithms-in-the-engine)
4. [CriptoChat – User Interface](#criptochat--user-interface)
5. [Project Structure](#project-structure)
6. [Installation](#installation)
7. [Quick Start](#quick-start)
8. [Running the Tests](#running-the-tests)
9. [Contributing](#contributing)
10. [License](#license)

---

## ✨ Introduction

MAE is a **self‑contained modular‑arithmetic library** implementing classical and modern number‑theoretic algorithms. It was created for educational purposesas part of a Discrete Mathematics course. MAE acts as a cryptographic back-end for CriptoChat, a simple terminal app with a user-based sytem that lets you send and recieve RSA‑encrypted messages.

---

## 🚀 Highlights

* **Deterministic primality** — Miller–Rabin test with smart base selection for strong pseudoprime test.
* **Advanced factorisation** — Pollard’s rho with *both* Floyd and Brent cycle‑detection variants, including `k`‑packet optimisation for fewer GCDs.
* **Complete RSA workflow** — key generation, padding, encryption/decryption, plus didactic attacks (plaintext, small‑e, cycle …).
* **Human‑friendly CLI** — CriptoChat stores contacts & keys in JSON, supports login/registration and graceful `Ctrl‑C` exit.
* **Extensive tests** — ≥ stress files up to 10⁶ cases.
* **Performance** — This projects grade included a performance competition, where "oro" (gold) was awarded to implementations matching teacher's own code in speed, and MH (Honourable Mention) to those that improved that one ore more orders of magnitude further. MAE achieved 4 MH and 4 Oro awards (see [docs/tiempos.txt](docs/tiempos.txt)).

---

## 🛠️ Algorithms in the Engine

| Category           | Algorithms                                                                                                                                                                   |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 🔢 *Arithmetic*    | Euclidean & extended GCD, modular inverse, modular exponentiation (square‑and‑multiply), Chinese Remainder Theorem solver                                                    |
| 📜 *Primality*     | Sieve of Eratosthenes, deterministic Miller–Rabin (64‑bit), strong pseudoprime test (SPRP), **Legendre/Jacobi symbols**                                                      |
| 🧩 *Factorisation* | **Pollard’s ρ (Floyd)**, **Pollard’s ρ (Brent)**, trial division with wheel 2 × 3 × 5 optimisation                                                                           |
| 🏗️ *Algebraic*    | Euler’s φ and Carmichael λ, primitive‑root search, quadratic congruence solver (Tonelli‑Shanks & `p≡3 mod 4` shortcut)                                                       |
| 🔐 *RSA Toolkit*   | Key generation over safe primes, PKCS‑style numeric padding, encryption/decryption for integers & UTF‑8 strings, small‑exponent attack, cycle attack, known‑plaintext attack |

### 🔍 Deep‑Dive: Pollard’s ρ with Cycle Finding

Pollard’s ρ exploits pseudorandom sequences `x_{i+1} = f(x_i) (mod n)` to reveal a non‑trivial GCD when two iterates repeat mod a non‑prime factor.

```text
pollard_rho_floyd_module   # Floyd’s tortoise–hare   O(√p) time / O(1) mem
pollard_rho_brent_module   # Brent’s improved stride  fewer modular sqrs
```

Both variants accept a **custom polynomial** `g(x)` and seed, enabling analysis of sequence quality. The implementation caches modular squares and batches GCDs (`k`‑packet trick) for up to ✖︎3 speed‑ups.

---

## 💬 CriptoChat – User Interface

| Feature               | Description                                                                                         |
| --------------------- | --------------------------------------------------------------------------------------------------- |
| 🔑 **Account System** | Sign‑up/login with password; JSON persistence (`users.json`).                                       |
| 🔐 **Key Management** | Automatic RSA key‑pair generation on first login; regenerate on demand.                             |
| 📇 **Contacts**       | Add/remove contacts by username, view public keys.                                                  |
| ✉️ **Messaging**      | Encrypt with recipient’s public key; decrypt with your private key. Padding length is configurable. |
| 🖥️ **TUI controls**  | Clean menus, input validation, `Ctrl‑C` safe exit.                                                  |

---

## 📂 Project Structure

```
.
├── modular.py            # Core arithmetic engine (MAE)
├── rsa.py                # RSA wrapper around MAE
├── commands.py           # Parser for command‑style calls
├── criptochat.py         # Terminal chat application
├── tests/                # Unit & stress tests
├── docs/                 # Academic reports & timing
└── imatlab.py            # I/O module stress test
├── imatlab_benchmark.py  # Performance benchmark for imatlab.py
```

---

## ⚙️ Installation

```bash
# 1. Clone
$ git clone https://github.com/sergihrs/Modular-Arithmetic-Engine.git && cd Modular-Arithmetic-Engine

# 2. (Recommended) create virtualenv
$ python -m venv .venv && source .venv/bin/activate

# 3. Install requirements (only stdlib + NumPy needed)
$ pip install -r requirements.txt
```

---

## ▶️ Quick Start

### Launch the Engine in interactive mode

```bash
$ python -i modular.py
>>> es_primo(13837529385627319953343937580684599256138676829007872413733775908157681858996601)
True
>>> es_primo(6723491414232079669217292762853534915213*9083927901770677456124118929912569301531)
False
>>> factorizar(15997248152129*13153572661417)
{15997248152129: 1, 13153572661417: 1}
```

### Use CriptoChat

```bash
$ python criptochat.py
# Follow the on‑screen menu to register, add a contact and send your first encrypted hello 🙂
```

---