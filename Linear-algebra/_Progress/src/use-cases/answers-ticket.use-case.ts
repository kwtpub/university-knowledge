import inquirer from "inquirer";
import { STATUS } from "../enum/statusTicker.enum.js";
import { TicketModel } from "../models/ticket.model.js";
import { historyRepository } from "../repository/histoty.repository.js";
import { ticketRepository } from "../repository/ticket.repository.js";

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

const FIRST_PAIR_NUMBER = 1;
const LAST_PAIR_NUMBER = 25;
const PAIR_OFFSET = 25;

export async function answersTicketUseCase(): Promise<void> {
  const ticketRepo = new ticketRepository();
  const historyRepo = new historyRepository();

  const ticketPairs = selectOrderedTicketPairs(
    ticketRepo.getAll(),
    FIRST_PAIR_NUMBER,
    LAST_PAIR_NUMBER,
    PAIR_OFFSET,
  );
  if (ticketPairs.length === 0) {
    console.log("Билеты не найдены.");
    return;
  }

  const answers: AnswerResult[] = [];

  for (let pairIndex = 0; pairIndex < ticketPairs.length; pairIndex += 1) {
    const pair = ticketPairs[pairIndex]!;
    const [first, second] = pair;

    console.log(
      `\n########## Пара ${pairIndex + 1} из ${ticketPairs.length}: билеты ${first.numberTicket} и ${second.numberTicket} ##########\n`,
    );

    printTicket(first);
    printTicket(second);

    for (const ticket of pair) {
      const { status } = await inquirer.prompt<{ status: STATUS }>([
        {
          type: "select",
          name: "status",
          message: `Билет №${ticket.numberTicket} — как вы его знаете?`,
          choices: STATUS_CHOICES,
          pageSize: STATUS_CHOICES.length,
          loop: false,
        },
      ]);

      answers.push({ ticket, status });
    }
  }

  const updatedTickets = updateTicketsAnswers(ticketRepo.getAll(), answers);
  ticketRepo.saveAll(updatedTickets);

  const answeredIds = new Set(answers.map((answer) => answer.ticket._id));
  const answeredTickets = updatedTickets.filter((ticket) =>
    answeredIds.has(ticket._id),
  );
  historyRepo.addEntries(answeredTickets);
}

function selectOrderedTicketPairs(
  allTickets: TicketModel[],
  firstPairNumber: number,
  lastPairNumber: number,
  offset: number,
): [TicketModel, TicketModel][] {
  if (allTickets.length === 0) {
    return [];
  }

  const byNumber = new Map<number, TicketModel>();
  for (const ticket of allTickets) {
    byNumber.set(ticket.numberTicket, ticket);
  }

  if (lastPairNumber < firstPairNumber) {
    return [];
  }

  const pairs: [TicketModel, TicketModel][] = [];

  for (
    let firstNumber = firstPairNumber;
    firstNumber <= lastPairNumber;
    firstNumber += 1
  ) {
    const first = byNumber.get(firstNumber);
    const second = byNumber.get(firstNumber + offset);
    if (!first || !second) {
      continue;
    }

    pairs.push([first, second]);
  }

  return pairs;
}

function updateTicketsAnswers(
  allTickets: TicketModel[],
  answers: AnswerResult[],
): TicketModel[] {
  const answersByTicketId = new Map<number, STATUS[]>();
  for (const answer of answers) {
    const existing = answersByTicketId.get(answer.ticket._id);
    if (existing) {
      existing.push(answer.status);
      continue;
    }
    answersByTicketId.set(answer.ticket._id, [answer.status]);
  }

  return allTickets.map((ticket) => {
    const statuses = answersByTicketId.get(ticket._id);
    if (!statuses || statuses.length === 0) {
      return ticket;
    }

    const lastStatus = statuses[statuses.length - 1]!;
    return new TicketModel(
      ticket._id,
      ticket.numberTicket,
      ticket.theme,
      ticket.text,
      ticket.countAnswer + statuses.length,
      lastStatus,
    );
  });
}

function printTicket(ticket: TicketModel): void {
  console.log("\n========================");
  console.log(`Билет №${ticket.numberTicket}`);
  console.log(`Тема: ${ticket.theme}`);
  console.log(ticket.text);
  console.log("========================\n");
}
