# 📘 Cheat Sheet de Git & GitHub — Uso Diario

> Guía de referencia rápida con los comandos más usados en el día a día de desarrollo.

---

## 🔧 1. Configuración inicial

| Comando | Descripción |
|---|---|
| `git config --global user.name "Nombre"` | Configura tu nombre para los commits |
| `git config --global user.email "correo@ejemplo.com"` | Configura tu correo |
| `git config --list` | Muestra toda la configuración actual |
| `git config --global core.editor "code --wait"` | Define VS Code como editor por defecto |
| `git config --global init.defaultBranch main` | Define `main` como rama por defecto |

---

## 📁 2. Crear o clonar un repositorio

| Comando | Descripción |
|---|---|
| `git init` | Inicializa un repositorio nuevo en la carpeta actual |
| `git clone <url>` | Clona un repositorio remoto |
| `git clone <url> <carpeta>` | Clona en una carpeta con nombre específico |
| `git clone --depth 1 <url>` | Clona solo el último commit (más rápido) |

---

## 📌 3. Estado y cambios locales

| Comando | Descripción |
|---|---|
| `git status` | Muestra el estado del repo (cambios, staged, etc.) |
| `git diff` | Muestra diferencias no confirmadas (unstaged) |
| `git diff --staged` | Muestra diferencias ya en staging |
| `git diff <rama1>..<rama2>` | Compara dos ramas |
| `git add <archivo>` | Agrega un archivo específico al staging |
| `git add .` | Agrega todos los cambios al staging |
| `git add -p` | Agrega cambios de forma interactiva (por fragmentos) |
| `git restore <archivo>` | Descarta cambios locales de un archivo |
| `git restore --staged <archivo>` | Saca un archivo del staging (sin borrar cambios) |

---

## 💾 4. Commits

| Comando | Descripción |
|---|---|
| `git commit -m "mensaje"` | Crea un commit con mensaje |
| `git commit -am "mensaje"` | Agrega (solo archivos ya rastreados) y commitea en un paso |
| `git commit --amend` | Modifica el último commit (mensaje o contenido) |
| `git commit --amend --no-edit` | Agrega cambios al último commit sin cambiar el mensaje |
| `git log` | Historial de commits |
| `git log --oneline --graph --all` | Historial compacto y visual de todas las ramas |
| `git log -p -2` | Muestra los últimos 2 commits con sus diffs |
| `git show <hash>` | Muestra detalles de un commit específico |

---

## 🌿 5. Ramas (branches)

| Comando | Descripción |
|---|---|
| `git branch` | Lista ramas locales |
| `git branch -a` | Lista ramas locales y remotas |
| `git branch <nombre>` | Crea una rama nueva |
| `git checkout <rama>` | Cambia de rama |
| `git checkout -b <rama>` | Crea y cambia a una rama nueva |
| `git switch <rama>` | Cambia de rama (comando moderno) |
| `git switch -c <rama>` | Crea y cambia a una rama nueva (moderno) |
| `git branch -d <rama>` | Elimina una rama (si ya está fusionada) |
| `git branch -D <rama>` | Fuerza la eliminación de una rama |
| `git branch -m <nuevo-nombre>` | Renombra la rama actual |

---

## 🔀 6. Merge y Rebase

| Comando | Descripción |
|---|---|
| `git merge <rama>` | Fusiona una rama en la actual |
| `git merge --no-ff <rama>` | Fusiona creando siempre un commit de merge |
| `git rebase <rama>` | Reaplica tus commits sobre otra rama |
| `git rebase -i HEAD~<n>` | Rebase interactivo de los últimos n commits (editar/squash) |
| `git rebase --continue` | Continúa el rebase tras resolver conflictos |
| `git rebase --abort` | Cancela el rebase en curso |
| `git cherry-pick <hash>` | Aplica un commit específico de otra rama |

---

## ☁️ 7. Repositorios remotos (GitHub)

| Comando | Descripción |
|---|---|
| `git remote -v` | Muestra los remotos configurados |
| `git remote add origin <url>` | Vincula el repo local con uno remoto |
| `git remote set-url origin <url>` | Cambia la URL del remoto |
| `git fetch` | Descarga cambios del remoto sin fusionarlos |
| `git fetch --all` | Descarga cambios de todos los remotos |
| `git pull` | Descarga y fusiona cambios del remoto |
| `git pull --rebase` | Descarga cambios y rebasa en vez de mergear |
| `git push` | Sube tus commits al remoto |
| `git push -u origin <rama>` | Sube y vincula la rama local con la remota |
| `git push origin --delete <rama>` | Elimina una rama remota |
| `git push --force-with-lease` | Fuerza el push de forma segura (recomendado sobre `--force`) |

---

## 📦 8. Guardar cambios temporalmente (Stash)

| Comando | Descripción |
|---|---|
| `git stash` | Guarda cambios no confirmados temporalmente |
| `git stash -u` | Incluye archivos no rastreados |
| `git stash list` | Lista los stashes guardados |
| `git stash pop` | Aplica y elimina el último stash |
| `git stash apply` | Aplica el último stash sin eliminarlo |
| `git stash drop` | Elimina un stash específico |
| `git stash clear` | Elimina todos los stashes |

---

## 🕵️ 9. Inspección e historial

| Comando | Descripción |
|---|---|
| `git blame <archivo>` | Muestra quién modificó cada línea de un archivo |
| `git log --author="nombre"` | Filtra commits por autor |
| `git log --since="2 weeks ago"` | Filtra commits por fecha |
| `git log -- <archivo>` | Historial de commits de un archivo específico |
| `git reflog` | Historial de movimientos de HEAD (útil para recuperar cambios "perdidos") |

---

## ⏪ 10. Deshacer cambios

| Comando | Descripción | Nivel de riesgo |
|---|---|---|
| `git reset <archivo>` | Saca un archivo del staging | 🟢 Bajo |
| `git reset --soft HEAD~1` | Deshace el último commit, mantiene cambios en staging | 🟡 Medio |
| `git reset --mixed HEAD~1` | Deshace el commit y el staging, mantiene cambios en el working dir | 🟡 Medio |
| `git reset --hard HEAD~1` | Elimina el último commit y todos sus cambios | 🔴 Alto (irreversible) |
| `git revert <hash>` | Crea un commit nuevo que deshace uno anterior (seguro para ramas compartidas) | 🟢 Bajo |
| `git clean -fd` | Elimina archivos y carpetas no rastreados | 🔴 Alto (irreversible) |

---

## 🏷️ 11. Tags (versiones)

| Comando | Descripción |
|---|---|
| `git tag` | Lista tags existentes |
| `git tag v1.0.0` | Crea un tag ligero |
| `git tag -a v1.0.0 -m "mensaje"` | Crea un tag anotado |
| `git push origin v1.0.0` | Sube un tag específico |
| `git push origin --tags` | Sube todos los tags |
| `git tag -d v1.0.0` | Elimina un tag local |

---

## 🐙 12. GitHub CLI (`gh`) — flujo diario con GitHub

> Requiere tener instalado [GitHub CLI](https://cli.github.com/).

| Comando | Descripción |
|---|---|
| `gh auth login` | Inicia sesión en GitHub desde la terminal |
| `gh repo clone <usuario>/<repo>` | Clona un repositorio |
| `gh repo create <nombre>` | Crea un repositorio nuevo |
| `gh pr create` | Crea un pull request desde la rama actual |
| `gh pr list` | Lista pull requests abiertos |
| `gh pr view <número> --web` | Abre un PR en el navegador |
| `gh pr checkout <número>` | Descarga y cambia a la rama de un PR |
| `gh pr merge <número>` | Fusiona un pull request |
| `gh issue list` | Lista issues del repositorio |
| `gh issue create` | Crea un issue nuevo |
| `gh workflow list` | Lista los workflows de GitHub Actions |
| `gh run list` | Lista ejecuciones recientes de Actions |

---

## ⚡ 13. Flujo de trabajo típico (resumen diario)

```bash
git pull origin main                  # 1. Actualiza tu rama local
git switch -c feature/nueva-funcion   # 2. Crea una rama para tu tarea
# ... trabajas y editas archivos ...
git add .                             # 3. Agrega los cambios
git commit -m "feat: agrega X"        # 4. Confirma el commit
git push -u origin feature/nueva-funcion  # 5. Sube la rama
gh pr create                          # 6. Abre un Pull Request
# ... revisión y aprobación ...
git switch main && git pull           # 7. Vuelve a main y actualiza
git branch -d feature/nueva-funcion   # 8. Limpia la rama local
```

---

## 💡 14. Tips rápidos

- **Convención de mensajes de commit** (estilo [Conventional Commits](https://www.conventionalcommits.org/)):
  `feat:` nueva funcionalidad · `fix:` corrección de bug · `docs:` documentación · `refactor:` refactor sin cambio de comportamiento · `test:` pruebas · `chore:` tareas de mantenimiento.
- Usa `git status` constantemente — es tu mejor herramienta de orientación.
- Prefiere `git switch` y `git restore` sobre `git checkout` (más explícitos, menos ambiguos).
- Antes de un `push --force`, usa siempre `--force-with-lease` para no sobrescribir el trabajo de otros.
- Configura un `.gitignore` desde el inicio del proyecto (plantillas en [github.com/github/gitignore](https://github.com/github/gitignore)).
