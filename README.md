# IT Estimator UI (Next.js 14)

Готовый UI-проект для оценки ИТ-проектов на **Next.js 14 (App Router)**, **TypeScript**, **Tailwind CSS**, **shadcn/ui** (локальные компоненты), **lucide-react**.

## Что внутри

- Тёмная тема по умолчанию.
- Sidebar навигация:
  - Дашборд
  - Проекты
  - Роли и ставки
- Страницы:
  - `/` → редирект на `/dashboard`
  - `/dashboard` — KPI карточки, недавние проекты, быстрые действия
  - `/projects` — таблица проектов + пустое состояние
  - `/roles` — таблица ролей и ставок + пустое состояние
- Моковые данные в памяти (`lib/mock-data.ts`).

---

## Локальный запуск (опционально)

### 1) Установить зависимости

```bash
npm install
```

### 2) Запустить dev-сервер

```bash
npm run dev
```

Откройте: http://localhost:3000

### 3) Production build (проверка)

```bash
npm run build
npm run start
```

---

## Деплой на Vercel через Import Git Repository

### 1) Залейте проект в GitHub

Создайте новый репозиторий и запушьте код:

```bash
git init
git add .
git commit -m "Initial UI dashboard"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 2) Импорт в Vercel

1. Перейдите в [https://vercel.com/new](https://vercel.com/new)
2. Нажмите **Import Git Repository**.
3. Выберите ваш GitHub-репозиторий.
4. Framework Preset определится как **Next.js** автоматически.
5. Нажмите **Deploy**.

### 3) Готово

После билда получите production URL вида:

`https://<project-name>.vercel.app`

---

## Технологический стек

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui (локальные UI-компоненты)
- lucide-react
