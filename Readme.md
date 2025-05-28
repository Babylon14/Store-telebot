## Работа с ветками в Git (VS Code + GitLab)

### 1. Клонируй репозиторий (если еще не сделал)

```bash
git clone https://gitlab.pklabs.ru/your-namespace/your-repo.git
cd your-repo
```

---

### 2. Создай новую ветку для своей задачи

```bash
git checkout -b <название-ветки>
```

**Пример:**
`git checkout -b dev-picture`

---

### 3. Внеси необходимые изменения в код

---

### 4. Проверь изменённые файлы

```bash
git status
```

---

### 5. Добавь изменения в индекс

```bash
git add .
```

Или только нужные файлы:

```bash
git add путь/к/файлу1 путь/к/файлу2
```

---

### 6. Зафиксируй изменения (commit)

```bash
git commit -m "Краткое описание изменений"
```

**Пример:**
`git commit -m "Добавил поддержку загрузки изображений"`

---

### 7. Отправь ветку на сервер (push)

```bash
git push origin <название-ветки>
```

**Пример:**
`git push origin dev-picture`

---

### 8. Создай Merge Request (MR) в GitLab

1. Открой репозиторий на [gitlab.pklabs.ru](https://gitlab.pklabs.ru).
2. Перейди во вкладку "Merge Requests" или следуй уведомлению "Create merge request".
3. Создай MR из своей ветки в `main` или `master`.
4. Заполни описание, при необходимости попроси ревью.
5. Дождись одобрения или автоматических проверок.

---

## **Best Practices**

* **Работай только в своих ветках.**
* **Делай маленькие, логически завершённые коммиты.**
* **Давай осмысленные названия веткам и коммитам.**
* **Перед merge обновляй свою ветку из основной:**

  ```bash
  git pull origin main
  git push origin <название-ветки>
  ```

---

## **Частые команды**

```bash
# Проверить текущую ветку
git branch

# Переключиться на существующую ветку
git checkout <название-ветки>

# Посмотреть историю коммитов
git log --oneline
```

---

## **Полезные ссылки**

* [Документация GitLab](https://docs.gitlab.com/ee/user/project/merge_requests/)
* [Git - основы](https://git-scm.com/book/ru/v2)


