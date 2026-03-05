import inquirer from "inquirer";
import { STATUS } from "../enum/statusTicker.enum.js";
import { TicketModel } from "../models/ticket.model.js";
import { LearningProgressModel } from "../models/learning-progress.model.js";
import { historyRepository } from "../repository/histoty.repository.js";
import { ticketRepository } from "../repository/ticket.repository.js";
import { LearningProgressRepository } from "../repository/learning-progress.repository.js";

type AnswerResult = {
  ticket: TicketModel;
  status: STATUS;
};

const STATUS_CHOICES = [
  { name: "ХОРОШО — знаю уверенно", value: STATUS.GOOD, short: STATUS.GOOD },
  {
    name: "СРЕДНЕ — есть пробелы",
    value: STATUS.AVERAGE,
    short: STATUS.AVERAGE,
  },
  { name: "ПЛОХО — помню с трудом", value: STATUS.BAD, short: STATUS.BAD },
  { name: "НИКАК — не знаю", value: STATUS.NONE, short: STATUS.NONE },
];

export async function learningModeUseCase(): Promise<void> {
  const ticketRepo = new ticketRepository();
  const historyRepo = new historyRepository();
  const learningProgressRepo = new LearningProgressRepository();

  const allTickets = ticketRepo.getAll();
  const themes = getUniqueThemes(allTickets);

  const { selectedTheme } = await inquirer.prompt<{ selectedTheme: string }>([
    {
      type: "select",
      name: "selectedTheme",
      message: "Выберите тему для обучения:",
      choices: themes.map((theme) => ({
        name: `${theme} (${countTicketsByTheme(allTickets, theme)} билетов)`,
        value: theme,
        short: theme,
      })),
      pageSize: themes.length,
      loop: false,
    },
  ]);

  const themeTickets = allTickets.filter(
    (ticket) => ticket.theme === selectedTheme,
  );

  console.log(
    `\n📚 Тема: ${selectedTheme}\n📋 Билетов в теме: ${themeTickets.length}\n`,
  );

  const answers: AnswerResult[] = [];

  for (let i = 0; i < themeTickets.length; i++) {
    const ticket = themeTickets[i]!;

    printTicket(ticket, i + 1, themeTickets.length);

    const { action } = await inquirer.prompt<{
      action: "answer" | "skip" | "exit";
    }>([
      {
        type: "select",
        name: "action",
        message: "Что делать?",
        choices: [
          { name: "Ответить на билет", value: "answer", short: "Ответить" },
          { name: "Пропустить", value: "skip", short: "Пропустить" },
          { name: "Выйти из режима обучения", value: "exit", short: "Выход" },
        ],
        pageSize: 3,
        loop: false,
      },
    ]);

    if (action === "exit") {
      console.log("\n👋 Выход из режима обучения.\n");
      break;
    }

    if (action === "skip") {
      console.log("\n⏭️  Билет пропущен.\n");
      continue;
    }

    const { status } = await inquirer.prompt<{ status: STATUS }>([
      {
        type: "select",
        name: "status",
        message: "Как вы знаете этот билет?",
        choices: STATUS_CHOICES,
        pageSize: STATUS_CHOICES.length,
        loop: false,
      },
    ]);

    answers.push({ ticket, status });
    console.log(`\n✅ Ответ записан: ${status}\n`);
  }

  if (answers.length === 0) {
    console.log("\n📭 Вы не ответили ни на один билет.\n");
    return;
  }

  const updatedTickets = updateTicketsAnswers(ticketRepo.getAll(), answers);
  ticketRepo.saveAll(updatedTickets);

  const answeredIds = new Set(answers.map((answer) => answer.ticket._id));
  const answeredTickets = updatedTickets.filter((ticket) =>
    answeredIds.has(ticket._id),
  );
  historyRepo.addEntries(answeredTickets);

  saveLearningProgress(learningProgressRepo, answers);

  await generateLearningProgressMarkdown(learningProgressRepo, selectedTheme);

  console.log(
    `\n🎉 Обучение завершено! Отвечено на ${answers.length} билет(ов).\n`,
  );
}

function getUniqueThemes(tickets: TicketModel[]): string[] {
  const themesSet = new Set<string>();
  for (const ticket of tickets) {
    themesSet.add(ticket.theme);
  }
  return Array.from(themesSet);
}

function countTicketsByTheme(tickets: TicketModel[], theme: string): number {
  return tickets.filter((ticket) => ticket.theme === theme).length;
}

function updateTicketsAnswers(
  allTickets: TicketModel[],
  answers: AnswerResult[],
): TicketModel[] {
  return allTickets.map((ticket) => {
    const answer = answers.find((item) => item.ticket._id === ticket._id);
    if (!answer) {
      return ticket;
    }

    return new TicketModel(
      ticket._id,
      ticket.numberTicket,
      ticket.theme,
      ticket.text,
      ticket.countAnswer + 1,
      answer.status,
    );
  });
}

function printTicket(
  ticket: TicketModel,
  current: number,
  total: number,
): void {
  console.log("\n" + "=".repeat(80));
  console.log(`📍 Билет ${current} из ${total}`);
  console.log(`🎫 Билет №${ticket.numberTicket}`);
  console.log(`📚 Тема: ${ticket.theme}`);
  console.log(`❓ ${ticket.text}`);
  console.log(`📊 Количество ответов: ${ticket.countAnswer}`);
  console.log(`📈 Текущий статус: ${ticket.understandingStatus}`);
  console.log("=".repeat(80));
}

function saveLearningProgress(
  repo: LearningProgressRepository,
  answers: AnswerResult[],
): void {
  const now = new Date().toISOString();

  for (const answer of answers) {
    const existingProgress = repo
      .getAll()
      .find((item) => item.ticketId === answer.ticket._id);

    const attemptCount = existingProgress
      ? existingProgress.attemptCount + 1
      : 1;

    const progress = new LearningProgressModel(
      existingProgress ? existingProgress._id : repo.getNextId(),
      answer.ticket._id,
      answer.ticket.numberTicket,
      answer.ticket.theme,
      answer.ticket.text,
      answer.status,
      attemptCount,
      now,
    );

    repo.addOrUpdate(progress);
  }
}

async function generateLearningProgressMarkdown(
  repo: LearningProgressRepository,
  theme: string,
): Promise<void> {
  const fs = await import("fs");
  const path = await import("path");
  const { fileURLToPath } = await import("url");

  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const outputPath = path.join(
    __dirname,
    "../../",
    `Прогресс_обучения_${sanitizeFileName(theme)}.md`,
  );

  const themeProgress = repo.getByTheme(theme);

  if (themeProgress.length === 0) {
    return;
  }

  const grouped = groupByStatus(themeProgress);

  let markdown = `# 📚 Прогресс обучения: ${theme}\n\n`;
  markdown += `*Последнее обновление: ${new Date().toLocaleString("ru-RU")}*\n\n`;
  markdown += `---\n\n`;

  const stats = calculateStats(themeProgress);
  markdown += `## 📊 Статистика\n\n`;
  markdown += `- **Всего билетов в обучении:** ${themeProgress.length}\n`;
  markdown += `- **ХОРОШО (✅):** ${stats.good} (${stats.goodPercent}%)\n`;
  markdown += `- **СРЕДНЕ (⚠️):** ${stats.average} (${stats.averagePercent}%)\n`;
  markdown += `- **ПЛОХО (❌):** ${stats.bad} (${stats.badPercent}%)\n`;
  markdown += `- **НИКАК (❓):** ${stats.none} (${stats.nonePercent}%)\n\n`;
  markdown += `---\n\n`;

  const statusOrder = [STATUS.GOOD, STATUS.AVERAGE, STATUS.BAD, STATUS.NONE];
  const statusEmoji = {
    [STATUS.GOOD]: "✅",
    [STATUS.AVERAGE]: "⚠️",
    [STATUS.BAD]: "❌",
    [STATUS.NONE]: "❓",
  };

  for (const status of statusOrder) {
    const tickets = grouped[status] || [];
    if (tickets.length === 0) continue;

    markdown += `## ${statusEmoji[status]} ${status} (${tickets.length})\n\n`;

    for (const ticket of tickets) {
      markdown += `### Билет №${ticket.numberTicket}\n`;
      markdown += `**Текст:** ${ticket.text}\n\n`;
      markdown += `- **Попыток:** ${ticket.attemptCount}\n`;
      markdown += `- **Последняя попытка:** ${new Date(ticket.lastAttemptDate).toLocaleString("ru-RU")}\n\n`;
      markdown += `---\n\n`;
    }
  }

  fs.writeFileSync(outputPath, markdown, "utf-8");
  console.log(`\n📝 Прогресс сохранён в: ${outputPath}\n`);
}

function sanitizeFileName(fileName: string): string {
  return fileName.replace(/[/\\?%*:|"<>]/g, "_");
}

function groupByStatus(
  progress: LearningProgressModel[],
): Record<STATUS, LearningProgressModel[]> {
  const grouped: Record<STATUS, LearningProgressModel[]> = {
    [STATUS.GOOD]: [],
    [STATUS.AVERAGE]: [],
    [STATUS.BAD]: [],
    [STATUS.NONE]: [],
  };

  for (const item of progress) {
    grouped[item.understandingStatus].push(item);
  }

  return grouped;
}

function calculateStats(progress: LearningProgressModel[]): {
  good: number;
  average: number;
  bad: number;
  none: number;
  goodPercent: string;
  averagePercent: string;
  badPercent: string;
  nonePercent: string;
} {
  const total = progress.length;
  const good = progress.filter((p) => p.understandingStatus === STATUS.GOOD)
    .length;
  const average = progress.filter(
    (p) => p.understandingStatus === STATUS.AVERAGE,
  ).length;
  const bad = progress.filter((p) => p.understandingStatus === STATUS.BAD)
    .length;
  const none = progress.filter((p) => p.understandingStatus === STATUS.NONE)
    .length;

  return {
    good,
    average,
    bad,
    none,
    goodPercent: ((good / total) * 100).toFixed(1),
    averagePercent: ((average / total) * 100).toFixed(1),
    badPercent: ((bad / total) * 100).toFixed(1),
    nonePercent: ((none / total) * 100).toFixed(1),
  };
}
