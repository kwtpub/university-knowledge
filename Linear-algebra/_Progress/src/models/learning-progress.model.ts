import { STATUS } from "../enum/statusTicker.enum.js";

export class LearningProgressModel {
  constructor(
    public readonly _id: number,
    public readonly ticketId: number,
    public readonly numberTicket: number,
    public readonly theme: string,
    public readonly text: string,
    public readonly understandingStatus: STATUS,
    public readonly attemptCount: number,
    public readonly lastAttemptDate: string,
  ) {}

  toJSON(): Record<string, unknown> {
    return {
      _id: this._id,
      ticketId: this.ticketId,
      numberTicket: this.numberTicket,
      theme: this.theme,
      text: this.text,
      understandingStatus: this.understandingStatus,
      attemptCount: this.attemptCount,
      lastAttemptDate: this.lastAttemptDate,
    };
  }

  static fromJSON(data: Record<string, unknown>): LearningProgressModel {
    return new LearningProgressModel(
      data._id as number,
      data.ticketId as number,
      data.numberTicket as number,
      data.theme as string,
      data.text as string,
      data.understandingStatus as STATUS,
      data.attemptCount as number,
      data.lastAttemptDate as string,
    );
  }
}
