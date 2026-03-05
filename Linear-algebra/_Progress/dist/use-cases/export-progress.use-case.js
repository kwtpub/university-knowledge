import { writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { STATUS } from "../enum/statusTicker.enum.js";
import { ticketRepository } from "../repository/ticket.repository.js";
export function exportProgressToMarkdown(outputPath = resolve(process.cwd(), "PROGRESS.md")) {
    const repo = new ticketRepository();
    const tickets = repo.getAll();
    const markdown = generateMarkdown(tickets);
    writeFileSync(outputPath, markdown, "utf-8");
}
function generateMarkdown(tickets) {
    const stats = calculateStats(tickets);
    const groupedByTheme = groupTicketsByTheme(tickets);
    let md = "# 📊 Прогресс по билетам — Математический анализ\n\n";
    md += `> Последнее обновление: ${new Date().toLocaleString("ru-RU")}\n\n`;
    md += "---\n\n";
    // Общая статистика
    md += "## 📈 Общая статистика\n\n";
    md += `- **Всего билетов:** ${stats.total}\n`;
    md += `- **Ответов дано:** ${stats.totalAnswers}\n`;
    md += `- **Средняя готовность:** ${stats.averageAnswers.toFixed(1)} ответов/билет\n\n`;
    // Статистика по статусам
    md += "### Статус понимания\n\n";
    md += "| Статус | Количество | Процент |\n";
    md += "|--------|-----------|--------|\n";
    md += `| ✅ ${STATUS.GOOD} | ${stats.byStatus[STATUS.GOOD]} | ${((stats.byStatus[STATUS.GOOD] / stats.total) * 100).toFixed(1)}% |\n`;
    md += `| 🟡 ${STATUS.AVERAGE} | ${stats.byStatus[STATUS.AVERAGE]} | ${((stats.byStatus[STATUS.AVERAGE] / stats.total) * 100).toFixed(1)}% |\n`;
    md += `| 🔴 ${STATUS.BAD} | ${stats.byStatus[STATUS.BAD]} | ${((stats.byStatus[STATUS.BAD] / stats.total) * 100).toFixed(1)}% |\n`;
    md += `| ❌ ${STATUS.NONE} | ${stats.byStatus[STATUS.NONE]} | ${((stats.byStatus[STATUS.NONE] / stats.total) * 100).toFixed(1)}% |\n\n`;
    // Прогресс-бар
    md += "### Прогресс\n\n";
    md += generateProgressBar(stats);
    md += "\n\n";
    md += "---\n\n";
    // Билеты по темам
    md += "## 📚 Билеты по темам\n\n";
    for (const [theme, themeTickets] of Object.entries(groupedByTheme)) {
        const themeStats = calculateThemeStats(themeTickets);
        md += `### ${theme}\n\n`;
        md += `> Билеты: ${themeTickets.length} | `;
        md += `Всего ответов: ${themeStats.totalAnswers} | `;
        md += `Средняя готовность: ${themeStats.averageAnswers.toFixed(1)}\n\n`;
        md += "| № | Текст билета | Ответов | Статус |\n";
        md += "|---|-------------|---------|--------|\n";
        for (const ticket of themeTickets) {
            const statusIcon = getStatusIcon(ticket.understandingStatus);
            const ticketNumber = `**${ticket.numberTicket}**`;
            const answerCount = `**${ticket.countAnswer}**`;
            md += `| ${ticketNumber} | ${ticket.text} | ${answerCount} | ${statusIcon} ${ticket.understandingStatus} |\n`;
        }
        md += "\n";
    }
    md += "---\n\n";
    // Таблица для Obsidian (dataview-friendly)
    md += "## 📋 Детальная таблица (для Obsidian Dataview)\n\n";
    md += "```dataview\n";
    md += "TABLE\n";
    md += '  numberTicket as "№",\n';
    md += '  theme as "Тема",\n';
    md += '  countAnswer as "Ответов",\n';
    md += '  understandingStatus as "Статус"\n';
    md += "FROM #билет\n";
    md += "SORT numberTicket ASC\n";
    md += "```\n\n";
    // Билеты, требующие внимания
    md += "---\n\n";
    md += "## ⚠️ Требуют внимания\n\n";
    const needAttention = tickets.filter((t) => t.understandingStatus === STATUS.NONE || t.countAnswer === 0);
    if (needAttention.length > 0) {
        md += "### Неизученные или не отвеченные\n\n";
        for (const ticket of needAttention) {
            md += `- [ ] **Билет ${ticket.numberTicket}**: ${ticket.text} (${ticket.countAnswer} ответов, статус: ${ticket.understandingStatus})\n`;
        }
        md += "\n";
    }
    else {
        md += "*Отлично! Все билеты были изучены хотя бы раз.*\n\n";
    }
    md += "---\n\n";
    md += "*Этот файл генерируется автоматически при обновлении прогресса.*\n";
    return md;
}
function calculateStats(tickets) {
    const total = tickets.length;
    const totalAnswers = tickets.reduce((sum, t) => sum + t.countAnswer, 0);
    const averageAnswers = total > 0 ? totalAnswers / total : 0;
    const byStatus = {
        [STATUS.GOOD]: tickets.filter((t) => t.understandingStatus === STATUS.GOOD)
            .length,
        [STATUS.AVERAGE]: tickets.filter((t) => t.understandingStatus === STATUS.AVERAGE).length,
        [STATUS.BAD]: tickets.filter((t) => t.understandingStatus === STATUS.BAD)
            .length,
        [STATUS.NONE]: tickets.filter((t) => t.understandingStatus === STATUS.NONE)
            .length,
    };
    return { total, totalAnswers, averageAnswers, byStatus };
}
function calculateThemeStats(tickets) {
    const totalAnswers = tickets.reduce((sum, t) => sum + t.countAnswer, 0);
    const averageAnswers = tickets.length > 0 ? totalAnswers / tickets.length : 0;
    return { totalAnswers, averageAnswers };
}
function groupTicketsByTheme(tickets) {
    const grouped = {};
    for (const ticket of tickets) {
        if (!grouped[ticket.theme]) {
            grouped[ticket.theme] = [];
        }
        grouped[ticket.theme].push(ticket);
    }
    return grouped;
}
function getStatusIcon(status) {
    switch (status) {
        case STATUS.GOOD:
            return "✅";
        case STATUS.AVERAGE:
            return "🟡";
        case STATUS.BAD:
            return "🔴";
        case STATUS.NONE:
            return "❌";
        default:
            return "⚪";
    }
}
function generateProgressBar(stats) {
    const total = stats.total;
    const good = stats.byStatus[STATUS.GOOD];
    const average = stats.byStatus[STATUS.AVERAGE];
    const bad = stats.byStatus[STATUS.BAD];
    const barLength = 40;
    const goodLength = Math.round((good / total) * barLength);
    const averageLength = Math.round((average / total) * barLength);
    const badLength = Math.round((bad / total) * barLength);
    const noneLength = barLength - goodLength - averageLength - badLength;
    const bar = [
        "✅".repeat(goodLength),
        "🟡".repeat(averageLength),
        "🔴".repeat(badLength),
        "⚪".repeat(Math.max(0, noneLength)),
    ].join("");
    return `\`\`\`\n${bar}\n\`\`\``;
}
